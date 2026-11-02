from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="owner", first_name="Alpha", license_number="OWN00001"
        )
        cls.manufacturers = []
        cls.cars = []
        cls.drivers = []

        for number in range(1, 5):
            manufacturer = Manufacturer.objects.create(
                name=f"Alpha {number}", country="Germany"
            )
            cls.manufacturers.append(manufacturer)
            cls.cars.append(Car.objects.create(
                model=f"Alpha {number}", manufacturer=manufacturer
            ))
            cls.drivers.append(get_user_model().objects.create_user(
                username=f"alpha{number}",
                license_number=f"TST{number:05d}",
            ))

        cls.other_manufacturer = Manufacturer.objects.create(
            name="Other", country="Alpha"
        )
        cls.other_car = Car.objects.create(
            model="Other", manufacturer=cls.manufacturers[0]
        )

    def setUp(self):
        self.client.force_login(self.user)
        self.cases = (
            ("manufacturer", "name", self.manufacturers,
             self.other_manufacturer),
            ("car", "model", self.cars, self.other_car),
            ("driver", "username", self.drivers, self.user),
        )

    def test_lists_require_login(self):
        self.client.logout()
        for entity, _, _, _ in self.cases:
            with self.subTest(entity=entity):
                url = reverse(f"taxi:{entity}-list")
                response = self.client.get(url)

                self.assertRedirects(
                    response, f"{reverse('login')}?next={url}"
                )

    def test_lists_without_search_and_with_empty_query(self):
        for entity, field, matches, other in self.cases:
            for params in ({}, {field: ""}):
                with self.subTest(entity=entity, params=params):
                    response = self.client.get(
                        reverse(f"taxi:{entity}-list"), params
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(
                        response, f"taxi/{entity}_list.html"
                    )
                    self.assertEqual(
                        response.context["paginator"].count, 5
                    )
                    self.assertEqual(
                        list(response.context[f"{entity}_list"]),
                        matches[:3],
                    )
                    second = self.client.get(
                        reverse(f"taxi:{entity}-list"),
                        {**params, "page": 2},
                    )
                    self.assertEqual(
                        list(second.context[f"{entity}_list"]),
                        [matches[3], other],
                    )

    def test_search_is_partial_case_insensitive_and_trimmed(self):
        for entity, field, matches, _ in self.cases:
            for query in ("AlPhA", "lph", "  alpha  "):
                with self.subTest(entity=entity, query=query):
                    response = self.client.get(
                        reverse(f"taxi:{entity}-list"), {field: query}
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response.context["paginator"].count, 4
                    )
                    self.assertEqual(
                        list(response.context[f"{entity}_list"]),
                        matches[:3],
                    )
                    self.assertEqual(
                        response.context["search_form"][field].value(),
                        query,
                    )

    def test_search_without_matches(self):
        for entity, field, _, _ in self.cases:
            with self.subTest(entity=entity):
                response = self.client.get(
                    reverse(f"taxi:{entity}-list"), {field: "missing"}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context[f"{entity}_list"]), []
                )

    def test_search_is_preserved_in_pagination(self):
        for entity, field, matches, _ in self.cases:
            with self.subTest(entity=entity):
                url = reverse(f"taxi:{entity}-list")
                first = self.client.get(url, {field: "AlPhA"})
                self.assertContains(first, f"{field}=AlPhA&amp;page=2")
                second = self.client.get(
                    url, {field: "AlPhA", "page": 2}
                )
                self.assertEqual(
                    list(second.context[f"{entity}_list"]), [matches[3]]
                )
                self.assertContains(second, f"{field}=AlPhA&amp;page=1")

    def test_invalid_query_shows_form_error(self):
        for entity, field, _, _ in self.cases:
            with self.subTest(entity=entity):
                response = self.client.get(
                    reverse(f"taxi:{entity}-list"), {field: "a" * 256}
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(field, response.context["search_form"].errors)


class CoreViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="owner", license_number="OWN00001"
        )
        cls.driver = get_user_model().objects.create_user(
            username="other", license_number="OTH00001"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        cls.car = Car.objects.create(
            model="A4", manufacturer=cls.manufacturer
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_counts_and_visits(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        for key, expected in (
            ("num_drivers", 2), ("num_cars", 1),
            ("num_manufacturers", 1), ("num_visits", 1),
        ):
            self.assertEqual(response.context[key], expected)
        self.assertEqual(self.client.get(url).context["num_visits"], 2)

    def test_create_driver(self):
        data = {
            "username": "new_user",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "NEW12345",
        }
        response = self.client.post(reverse("taxi:driver-create"), data)
        driver = get_user_model().objects.get(username="new_user")
        self.assertRedirects(response, driver.get_absolute_url())

        for field in ("first_name", "last_name", "license_number"):
            self.assertEqual(getattr(driver, field), data[field])
        self.assertTrue(driver.check_password(data["password1"]))

    def test_update_license(self):
        response = self.client.post(
            reverse("taxi:driver-update", args=[self.driver.pk]),
            {"license_number": "NEW54321"},
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "NEW54321")

    def test_invalid_license_does_not_update_driver(self):
        response = self.client.post(
            reverse("taxi:driver-update", args=[self.driver.pk]),
            {"license_number": "invalid"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "license_number", response.context["form"].errors
        )
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "OTH00001")

    def test_delete_driver_redirects_and_removes_relation(self):
        self.car.drivers.add(self.driver)
        response = self.client.post(
            reverse("taxi:driver-delete", args=[self.driver.pk])
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(
            get_user_model().objects.filter(pk=self.driver.pk).exists()
        )
        self.assertFalse(self.car.drivers.exists())

    def test_car_creation_and_update_save_drivers(self):
        data = {
            "model": "A6", "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk],
        }
        response = self.client.post(reverse("taxi:car-create"), data)
        self.assertRedirects(response, reverse("taxi:car-list"))
        car = Car.objects.get(model="A6")
        self.assertEqual(list(car.drivers.all()), [self.user])
        response = self.client.post(
            reverse("taxi:car-update", args=[car.pk]),
            {**data, "drivers": [self.driver.pk]},
        )
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(list(car.drivers.all()), [self.driver])

    def test_toggle_assignment(self):
        self.car.drivers.add(self.driver)
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])
        for expected in (True, False):
            response = self.client.post(url)
            self.assertRedirects(
                response,
                reverse("taxi:car-detail", args=[self.car.pk])
            )
            self.assertEqual(
                self.car.drivers.filter(pk=self.user.pk).exists(), expected
            )
            self.assertTrue(
                self.car.drivers.filter(pk=self.driver.pk).exists()
            )

    def test_toggle_requires_login(self):
        self.client.logout()
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])
        response = self.client.post(url)
        self.assertRedirects(
            response, f"{reverse('login')}?next={url}"
        )
        self.assertFalse(self.car.drivers.exists())

    def test_toggle_rejects_get(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 405)
        self.assertFalse(self.car.drivers.exists())

    def test_toggle_missing_car_returns_404(self):
        missing_pk = self.car.pk + 1
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[missing_pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_assignment_form_sends_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        detail_url = reverse("taxi:car-detail", args=[self.car.pk])
        response = client.get(detail_url)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        token = client.cookies["csrftoken"].value
        response = client.post(
            reverse("taxi:toggle-car-assign", args=[self.car.pk]),
            {"csrfmiddlewaretoken": token},
        )
        self.assertRedirects(response, detail_url)
        self.assertTrue(self.car.drivers.filter(pk=self.user.pk).exists())

    def test_sidebar_logout_form(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertContains(
            response, f'<form method="post" action="{reverse("logout")}">'
        )
        response = self.client.post(reverse("logout"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
