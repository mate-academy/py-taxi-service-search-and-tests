from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicCarTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="testname")

    def test_retrieve_cars(self):
        Car.objects.create(model="testmodel", manufacturer=self.manufacturer)
        Car.objects.create(model="testmodel2", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        test_user = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(test_user.first_name, form_data["first_name"])
        self.assertEqual(test_user.last_name, form_data["last_name"])
        self.assertEqual(test_user.license_number, form_data["license_number"])

    def test_create_driver_with_incorrect_license_number(self):
        url = reverse("taxi:driver-create")
        response = self.client.post(
            url,
            {
                "username": "testuser",
                "password1": "password123",
                "password2": "password123",
                "license_number": "invalid",
                "first_name": "testt",
                "last_name": "testtt",
            },
        )

        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"],
        )


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.force_login(self.user)
        for i in range(11):
            Manufacturer.objects.create(
                name=f"testname{i}",
                country=f"testcountry{i}"
            )

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(
                response.context["manufacturer_list"]
            ), list(manufacturers)[:5]
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_by_page(self):
        response = self.client.get(MANUFACTURER_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(
                response.context["manufacturer_list"]
            ), list(manufacturers)[5:10]
        )

    def test_update_manufacturer(self):
        payload = {
            "name": "unique_name_test",
            "country": "test_USA"
        }
        manufacturer = Manufacturer.objects.all().first()
        manufacturer_url = reverse(
            "taxi:manufacturer-update",
            args=[manufacturer.pk]
        )
        response = self.client.post(manufacturer_url, payload)
        self.assertEqual(response.status_code, 302)
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, payload.get("name"))
        self.assertEqual(manufacturer.country, payload.get("country"))
