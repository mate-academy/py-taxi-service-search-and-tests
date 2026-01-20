from django.test import TestCase
from taxi.forms import DriverCreationForm


class DriverFormTests(TestCase):
    def test_driver_creation_form_with_all_fields(self):
        form_data = {
            "username": "test_driver",
            "password1": "Password_test!",
            "password2": "Password_test!",
            "license_number": "ABC12345",
            "first_name": "test_first",
            "last_name": "test_last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
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
