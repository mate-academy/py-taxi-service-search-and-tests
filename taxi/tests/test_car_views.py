from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class TestCarListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Porsche",
            country="Germany", )

        self.url = reverse("taxi:car-list")

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_can_not_access(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_context_of_list(self):
        self.client.force_login(self.user)
        gt = Car.objects.create(model="911 GT",
                                manufacturer=self.manufacturer)
        carrera = Car.objects.create(model="Carrera",
                                     manufacturer=self.manufacturer)

        response = self.client.get(self.url)

        cars = response.context["car_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Car.objects.count(), 2)
        self.assertIn(gt, cars)
        self.assertIn(carrera, cars)

    def test_uses_correct_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_by_model_with_query_param(self):
        self.client.force_login(self.user)
        rs6 = Car.objects.create(model="RS6",
                                 manufacturer=self.manufacturer)
        tt = Car.objects.create(model="TT",
                                manufacturer=self.manufacturer)

        response = self.client.get(self.url, {"model": "rs6"})

        cars = response.context["car_list"]

        self.assertEqual(cars.count(), 1)
        self.assertIn(rs6, cars)
        self.assertNotIn(tt, cars)

    def test_search_by_model_without_query_param(self):
        self.client.force_login(self.user)
        rs6 = Car.objects.create(model="RS6",
                                 manufacturer=self.manufacturer)
        tt = Car.objects.create(model="TT",
                                manufacturer=self.manufacturer)

        response = self.client.get(self.url)

        cars = response.context["car_list"]

        self.assertEqual(cars.count(), 2)
        self.assertIn(rs6, cars)
        self.assertIn(tt, cars)

    def test_pagination(self):
        self.client.force_login(self.user)
        for i in range(6):
            manufacturer = Manufacturer.objects.create(
                name=f"manufacturer{i}",
                country="poland")
            Car.objects.create(
                model=f"car{i}",
                manufacturer=manufacturer)

        response = self.client.get(self.url)
        cars = response.context["car_list"]
        page_obj = response.context["page_obj"]

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(cars.count(), 5)
        self.assertEqual(page_obj.number, 1)
        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())

    def test_pagination_next_pages(self):
        self.client.force_login(self.user)
        for i in range(6):
            manufacturer = Manufacturer.objects.create(
                name=f"manufacturer{i}",
                country="poland")
            Car.objects.create(
                model=f"car{i}",
                manufacturer=manufacturer)

        response = self.client.get(self.url, {"page": 2})
        cars = response.context["car_list"]
        page_obj = response.context["page_obj"]

        self.assertEqual(cars.count(), 1)
        self.assertEqual(page_obj.number, 2)
        self.assertFalse(page_obj.has_next())
        self.assertTrue(page_obj.has_previous())


class TestCarCreateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany", )
        self.url = reverse("taxi:car-create")

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_creation_of_car(self):
        self.client.force_login(self.user)

        self.assertEqual(Car.objects.count(), 0)

        response = self.client.post(
            self.url,
            {"model": "M5",
             "manufacturer": self.manufacturer.pk,
             "drivers": [self.user.pk]
             }
        )

        car = Car.objects.get(model="M5")

        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(car.model, "M5")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertIn(
            self.user,
            car.drivers.all()
        )


class TestCarUpdateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer, )
        self.car.drivers.add(self.user)

        self.url = reverse(
            "taxi:car-update",
            kwargs={"pk": self.car.pk})

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        self.assertEqual(response.status_code, 302)

    def test_updating_an_existing_car(self):
        self.client.force_login(self.user)
        porsche = Manufacturer.objects.create(name="Porsche",
                                              country="Germany")

        response = self.client.post(self.url, {"model": "Panamera",
                                               "manufacturer": porsche.pk,
                                               "drivers": [self.user.pk]
                                               }
                                    )
        self.car.refresh_from_db()

        self.assertIn(self.user, self.car.drivers.all())
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(self.car.manufacturer, porsche)
        self.assertEqual(self.car.model, "Panamera")

        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_updating_with_incorrect_data(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {"model": "ALPINA M3",
             "manufacturer": self.manufacturer.pk,
             "drivers": ""})
        self.car.refresh_from_db()

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.car.model, "X5")
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertIn(self.user, self.car.drivers.all())
        self.assertEqual(Car.objects.count(), 1)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)


class TestCarDeleteView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345", )
        self.manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="Germany")
        self.car = Car.objects.create(
            model="Zafira",
            manufacturer=self.manufacturer)

        self.car.drivers.add(self.user)

        self.url = reverse("taxi:car-delete", kwargs={"pk": self.car.pk})

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        self.assertEqual(response.status_code, 302)

    def test_deleting_a_car(self):
        self.client.force_login(self.user)
        self.assertEqual(Car.objects.count(), 1)

        response = self.client.post(self.url)

        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())
        self.assertEqual(Car.objects.count(), 0)
        self.assertRedirects(response, reverse("taxi:car-list"))


class TestCarDetailView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345", )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan", )

        self.car = Car.objects.create(
            model="Aygo",
            manufacturer=self.manufacturer)

        self.car.drivers.add(self.user)

        self.url = reverse("taxi:car-detail", kwargs={"pk": self.car.pk})

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        self.assertEqual(response.status_code, 302)

    def test_get_detail_of_car(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        car = response.context["car"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(car, self.car)

    def test_nonexistent_car_returns_404(self):
        self.client.force_login(self.user)

        url = reverse(
            "taxi:car-detail",
            kwargs={"pk": 999999}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "taxi/car_detail.html")


class TestToggleAssignToCar(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345", )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany")
        self.car = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer)

        self.url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.pk})

    def test_anonymous_redirect_to_login(self):
        response = self.client.post(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        self.assertEqual(response.status_code, 302)

    def test_toggle_assigns_driver_to_car(self):
        self.client.force_login(self.user)

        self.assertNotIn(
            self.user,
            self.car.drivers.all()
        )

        response = self.client.post(self.url)

        self.assertIn(
            self.user,
            self.car.drivers.all()
        )
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk}))

    def test_toggle_removes_driver_from_car(self):
        self.client.force_login(self.user)

        self.car.drivers.add(self.user)

        self.assertIn(
            self.user,
            self.car.drivers.all()
        )

        response = self.client.post(self.url)

        self.assertNotIn(
            self.user,
            self.car.drivers.all()
        )

        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                kwargs={"pk": self.car.pk}
            )
        )
