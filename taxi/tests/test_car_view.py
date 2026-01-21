from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class CarListViewTest(TestCase):

    CAR_URL = reverse("taxi:car-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )
        number_of_cars = 13

        for i in range(number_of_cars):
            manufacturer = Manufacturer.objects.create(
                name=f"Test Manufacturer {i}", country="Test Country"
            )
            Car.objects.create(
                model=f"Test Model {i}",
                manufacturer=manufacturer,
            )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.CAR_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_pagination_is_five(self):
        self.client.force_login(self.user)
        response = self.client.get(self.CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_lists_all_cars(self):
        self.client.force_login(self.user)
        response = self.client.get(self.CAR_URL + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 3)


class CarSearchFormTest(TestCase):
    CAR_URL = reverse("taxi:car-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )
        number_of_cars = 13

        for i in range(number_of_cars):
            manufacturer = Manufacturer.objects.create(
                name=f"Test Manufacturer {i}", country="Test Country"
            )
            Car.objects.create(
                model=f"Test Model {i}",
                manufacturer=manufacturer,
            )

    def test_search_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.CAR_URL + "?model=Test")
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["model"], "Test"
        )

    def test_car_queryset_filtered_by_model(self):
        self.client.force_login(self.user)

        Car.objects.all().delete()
        manufacturer = Manufacturer.objects.create(
            name="Brand", country="Country"
        )
        Car.objects.create(model="BMW X5", manufacturer=manufacturer)
        Car.objects.create(model="Audi A6", manufacturer=manufacturer)
        Car.objects.create(model="Tesla Model S", manufacturer=manufacturer)

        response = self.client.get(self.CAR_URL + "?model=tesla")
        cars = response.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Tesla Model S")


class CarCreateViewTest(TestCase):
    CAR_URL = reverse("taxi:car-create")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.CAR_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_success_url(self):
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Another manufacturer", country="Country"
        )
        driver = Driver.objects.create(license_number="XYZ12345")

        form_data = {
            "model": "Another Car",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id],
        }
        response = self.client.post(reverse("taxi:car-create"), data=form_data)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertTrue(
            Car.objects.filter(
                model="Another Car", manufacturer=manufacturer
            ).exists()
        )
        self.assertEqual(Car.objects.count(), 1)

    def test_form_displayed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")
        self.assertContains(response, "model")

    def test_create_with_invalid_data(self):
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Another manufacturer", country="Country"
        )

        form_data = {
            "model": "Another Car",
            "manufacturer": manufacturer.id,
            # "drivers": driver.id
        }
        response = self.client.post(reverse("taxi:car-create"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "drivers", "This field is required."
        )
        self.assertEqual(Car.objects.count(), 0)


class CarDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="12345"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestMan", country="TestCountry"
        )
        cls.car = Car.objects.create(
            model="Test Car", manufacturer=cls.manufacturer
        )
        cls.car_url = reverse("taxi:car-detail", args=[cls.car.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.car_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.car_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertContains(response, "Test Car")

    def test_404_if_car_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class CarUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="TestMan", country="TestCountry"
        )
        cls.driver = Driver.objects.create(license_number="XYZ12345")

        cls.car = Car.objects.create(
            model="Test Car", manufacturer=cls.manufacturer
        )
        cls.car.drivers.set([cls.driver])

        cls.CAR_URL = reverse("taxi:car-update", args=[cls.car.id])

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.CAR_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template_after_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.CAR_URL,
            data={
                "model": "Test Car",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.driver.id],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertContains(response, "Test Car")

    def test_update_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse("taxi:car-update", args=[self.car.id])
        form_data = {
            "model": "Test Car",
            "manufacturer": self.manufacturer.id,

        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "drivers", "This field is required."
        )

        self.manufacturer.refresh_from_db()
        self.assertNotEqual(self.manufacturer.name, "")


class CarDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="pass123"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="TestMan", country="TestCountry"
        )
        cls.car = Car.objects.create(
            model="Delete Me", manufacturer=cls.manufacturer
        )
        cls.CAR_DELETE_URL_NAME = "taxi:car-delete"
        cls.url = reverse(cls.CAR_DELETE_URL_NAME, args=[cls.car.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_car(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())

    def test_template_used(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")
