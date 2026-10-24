from urllib.parse import parse_qs, urlsplit

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.html import escape

from .forms import DriverCreationForm, DriverLicenseUpdateForm
from .models import Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Alice", license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="Bob", license_number="DEF12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln", country="USA"
        )
        Manufacturer.objects.create(name="Toyota", country="Japan")
        self.car = Car.objects.create(
            model="Continental", manufacturer=self.manufacturer
        )
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        self.client.force_login(self.driver)
        self.cases = (
            ("driver", "username", "aLI", self.driver),
            ("car", "model", "tINen", self.car),
            ("manufacturer", "name", "iNCo", self.manufacturer),
        )

    def test_case_insensitive_partial_matches(self):
        for model, field, query, expected in self.cases:
            with self.subTest(model=model):
                response = self.client.get(
                    reverse(f"taxi:{model}-list"), {field: query}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context[f"{model}_list"]), [expected]
                )
                self.assertEqual(
                    response.context["search_form"][field].value(), query
                )

    def test_blank_and_missing_search_show_all_records(self):
        for model, field, _, _ in self.cases:
            for params in ({}, {field: ""}, {field: "  "}):
                with self.subTest(model=model, params=params):
                    response = self.client.get(
                        reverse(f"taxi:{model}-list"), params
                    )
                    self.assertEqual(response.context["paginator"].count, 2)

    def test_no_results_and_non_search_fields_are_not_matched(self):
        for model, field, query in (
            ("driver", "username", "ABC12345"),
            ("car", "model", "Lincoln"),
            ("manufacturer", "name", "USA"),
        ):
            with self.subTest(model=model):
                response = self.client.get(
                    reverse(f"taxi:{model}-list"), {field: query}
                )
                self.assertFalse(response.context[f"{model}_list"])
                self.assertContains(response, "match your search")

    def test_whitespace_is_trimmed(self):
        for model, field, query, expected in self.cases:
            with self.subTest(model=model):
                response = self.client.get(
                    reverse(f"taxi:{model}-list"), {field: f"  {query}  "}
                )
                self.assertEqual(
                    list(response.context[f"{model}_list"]), [expected]
                )

    def test_search_is_preserved_and_encoded_across_pages(self):
        term = "Match & More"
        for index in range(7):
            get_user_model().objects.create_user(
                username=f"{term}{index}", license_number=f"TST{index:05}"
            )
            Car.objects.create(
                model=f"{term}{index}", manufacturer=self.manufacturer
            )
            Manufacturer.objects.create(name=f"{term}{index}", country="US")
        for model, field, _, _ in self.cases:
            with self.subTest(model=model):
                url = reverse(f"taxi:{model}-list")
                first = self.client.get(url, {field: term})
                self.assertEqual(len(first.context[f"{model}_list"]), 5)
                query = first.context["search_query"]
                self.assertEqual(parse_qs(query), {field: [term]})
                self.assertContains(
                    first, escape(f"?{query}&page=2")
                )
                second = self.client.get(url, {field: term, "page": 2})
                self.assertEqual(second.context["paginator"].count, 7)
                self.assertEqual(len(second.context[f"{model}_list"]), 2)
                self.assertNotIn(
                    "page", parse_qs(second.context["search_query"])
                )
                self.assertFalse(
                    set(first.context[f"{model}_list"])
                    & set(second.context[f"{model}_list"])
                )

    def test_lists_require_login(self):
        self.client.logout()
        for model, _, _, _ in self.cases:
            response = self.client.get(reverse(f"taxi:{model}-list"))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                urlsplit(response.url).path, reverse("login")
            )

    def test_html_in_search_is_escaped(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": '<script>alert("x")</script>'}
        )
        self.assertNotContains(response, '<script>alert("x")</script>')
        self.assertContains(response, "&lt;script&gt;")


class CoreWorkflowTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver", license_number="ABC12345"
        )
        self.other = get_user_model().objects.create_user(
            username="other", license_number="DEF12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln", country="USA"
        )
        self.car = Car.objects.create(
            model="Continental", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.other)
        self.client.force_login(self.driver)

    def test_home_counts_and_session_visits(self):
        for visits in (1, 2):
            response = self.client.get(reverse("taxi:index"))
            self.assertEqual(response.context["num_visits"], visits)
            self.assertEqual(response.context["num_drivers"], 2)
            self.assertEqual(response.context["num_cars"], 1)
            self.assertEqual(response.context["num_manufacturers"], 1)

    def test_license_validation_applies_on_create_and_update(self):
        base = {
            "username": "new", "password1": "Unusual-password-7824",
            "password2": "Unusual-password-7824",
        }
        for number in (
            "ABC12345", "abC12345", "AB123456", "ABCD1234", "ABC123"
        ):
            valid = number == "ABC12345"
            for form in (
                DriverCreationForm(data={
                    **base, "license_number": number.replace("ABC", "XYZ")
                }),
                DriverLicenseUpdateForm(
                    data={"license_number": number}, instance=self.driver
                ),
            ):
                with self.subTest(number=number, form=type(form).__name__):
                    self.assertEqual(form.is_valid(), valid)

    def test_driver_creation_and_license_update(self):
        response = self.client.post(reverse("taxi:driver-create"), {
            "username": "new", "license_number": "NEW12345",
            "first_name": "New", "last_name": "Driver",
            "password1": "Unusual-password-7824",
            "password2": "Unusual-password-7824",
        })
        driver = get_user_model().objects.get(username="new")
        self.assertRedirects(response, driver.get_absolute_url())
        self.assertTrue(driver.check_password("Unusual-password-7824"))
        response = self.client.post(
            reverse("taxi:driver-update", args=[driver.pk]),
            {"license_number": "NEW54321"},
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
        driver.refresh_from_db()
        self.assertEqual(driver.license_number, "NEW54321")

    def test_driver_delete_preserves_car(self):
        url = reverse("taxi:driver-delete", args=[self.other.pk])
        self.assertContains(self.client.get(url), "Cancel")
        self.assertTrue(
            get_user_model().objects.filter(pk=self.other.pk).exists()
        )
        self.assertRedirects(
            self.client.post(url), reverse("taxi:driver-list")
        )
        self.assertFalse(
            get_user_model().objects.filter(pk=self.other.pk).exists()
        )
        self.assertTrue(Car.objects.filter(pk=self.car.pk).exists())
        self.assertFalse(self.car.drivers.exists())

    def test_car_creation_and_update_assignments(self):
        response = self.client.post(reverse("taxi:car-create"), {
            "model": "New car", "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver.pk],
        })
        self.assertRedirects(response, reverse("taxi:car-list"))
        car = Car.objects.get(model="New car")
        self.assertEqual(list(car.drivers.all()), [self.driver])
        response = self.client.post(
            reverse("taxi:car-update", args=[car.pk]),
            {"model": "Updated", "manufacturer": self.manufacturer.pk,
             "drivers": [self.other.pk]},
        )
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(list(car.drivers.all()), [self.other])

    def test_assignment_post_only_and_scoped_to_current_user(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(
            set(self.car.drivers.all()), {self.driver, self.other}
        )
        self.client.post(url)
        self.assertEqual(list(self.car.drivers.all()), [self.other])
        self.assertEqual(self.client.post(reverse(
            "taxi:toggle-car-assign", args=[999]
        )).status_code, 404)

    def test_assignment_requires_csrf_and_login(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.driver)
        self.assertEqual(client.post(url).status_code, 403)
        self.client.logout()
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(list(self.car.drivers.all()), [self.other])

    def test_invalid_car_does_not_save(self):
        response = self.client.post(reverse("taxi:car-create"), {
            "model": "", "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver.pk],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("model", response.context["form"].errors)
        self.assertEqual(Car.objects.count(), 1)

    def test_manufacturer_create_update_delete(self):
        response = self.client.post(reverse("taxi:manufacturer-create"), {
            "name": "Toyota", "country": "Japan",
        })
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        manufacturer = Manufacturer.objects.get(name="Toyota")
        self.client.post(reverse(
            "taxi:manufacturer-update", args=[manufacturer.pk]
        ), {"name": "Updated", "country": "Japan"})
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "Updated")
        self.assertRedirects(self.client.post(reverse(
            "taxi:manufacturer-delete", args=[manufacturer.pk]
        )), reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(pk=manufacturer.pk).exists()
        )

    def test_car_delete_only_mutates_on_post(self):
        url = reverse("taxi:car-delete", args=[self.car.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Car.objects.filter(pk=self.car.pk).exists())
        self.assertRedirects(self.client.post(url), reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())

    def test_mutation_views_require_login(self):
        self.client.logout()
        for model, instance in (
            ("driver", self.other), ("car", self.car),
            ("manufacturer", self.manufacturer),
        ):
            for action in ("create", "update", "delete"):
                args = [] if action == "create" else [instance.pk]
                url = reverse(f"taxi:{model}-{action}", args=args)
                for method in (self.client.get, self.client.post):
                    with self.subTest(url=url, method=method.__name__):
                        self.assertEqual(method(url).status_code, 302)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Manufacturer.objects.count(), 1)
        self.assertEqual(get_user_model().objects.count(), 2)
