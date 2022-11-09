from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_is_valid(self):
        form_data = {
            "username": "admin.user",
            "password1": "password_test123",
            "password2": "password_test123",
            "license_number": "TJK12345",
            "first_name": "Test first",
            "last_name": "Test last",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "admin.user",
            "password1": "password_test123",
            "password2": "password_test123",
            "license_number": "TJK12345",
            "first_name": "Test first",
            "last_name": "Test last",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
