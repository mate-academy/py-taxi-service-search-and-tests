from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(
            name="TestName1",
            country="TestCountry1"
        )
        Manufacturer.objects.create(
            name="TestName2",
            country="TestCountry2"
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            response.context["manufacturer_list"].count(),
            manufacturers.count()
        )


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "New_Driver",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "license_number": "AAA55555"
        }
        self.client.post(reverse("taxi:driver-create"), form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
