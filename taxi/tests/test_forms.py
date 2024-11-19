from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class FormTests(TestCase):
    def test_create_driver_with_all_fields(self):
        form_data = {
            "first_name": "First",
            "last_name": "Last",
            "username": "Username",
            "license_number": "AAA12345",
            "password1": "1qaz3edc",
            "password2": "1qaz3edc",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(
            form.cleaned_data["license_number"], form_data["license_number"]
        )

    def test_validate_license_number(self):
        license_number = "AAA12345"
        self.assertTrue(len(license_number) == 8)
        self.assertTrue(license_number[:3].isupper())
        self.assertTrue(license_number[:3].isalpha())
        self.assertTrue(license_number[3:].isdigit())
        self.assertTrue(validate_license_number(license_number))

    def test_invalid_license_number(self):
        license_number = "AAA123"
        self.assertRaises(
            ValidationError,
            validate_license_number,
            license_number
        )
