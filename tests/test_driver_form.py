from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormTests(TestCase):
    def test_driver_creation_form_with_additional_fields(self):
        form_data = {
            "username": "driver_username",
            "password1": "driver_password",
            "password2": "driver_password",
            "license_number": "ABC12345",
            "first_name": "driver_first_name",
            "last_name": "driver_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )

    def test_invalid_license_number(self):
        form_data = {
            "username": "driver_username",
            "password1": "driver_password",
            "password2": "driver_password",
            "license_number": "INVALID",
            "first_name": "driver_first_name",
            "last_name": "driver_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
