from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="manufacturer_name0",
            country="manufacturer_country0",
        )
        Manufacturer.objects.create(
            name="manufacturer_name1",
            country="manufacturer_country1",
        )
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )

    def test_private_driver(self):
        form_data = {
            "username": "new_user1",
            "password1": "user_password1",
            "password2": "user_password1",
            "first_name": "first_name1",
            "last_name": "last_name1",
            "license_number": "VDD12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
