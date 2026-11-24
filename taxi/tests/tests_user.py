from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver
from django.contrib.auth import get_user_model

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PrivateDriverTestlTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test12345", license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.form_data = {
            "username": "new_user",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "XYZ54321",
        }

    def test_create_driver_saves_custom_fields(self):
        self.client.post(DRIVER_CREATE_URL, data=self.form_data)
        new_user = get_user_model().objects.get(username="new_user")

        self.assertEqual(new_user.first_name, "John")
        self.assertEqual(new_user.last_name, "Smith")
        self.assertEqual(new_user.license_number, "XYZ54321")

    def test_create_driver_with_invalid_license_is_rejected(self):
        self.form_data["license_number"] = "bad"
        response = self.client.post(DRIVER_CREATE_URL, data=self.form_data)

        self.assertIn("license_number", response.context["form"].errors)
