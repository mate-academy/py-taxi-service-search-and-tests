from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverLicenseUpdateForm,
    DriverCreationForm,
    validate_license_number,
)


class TestDriverForms(TestCase):
    def test_driver_form_invalid_license_number(self):
        data = {
            "username": "interjkee",
            "password1": "111111",
            "password2": "111111",
            "license_number": "ABC1234",
            "first_name": "Alex",
            "last_name": "Chalaidiuk",
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_form_valid_license_number(self):
        data = {
            "username": "interjkee",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12345",
            "first_name": "Alex",
            "last_name": "Chalaidiuk",
        }
        form = DriverCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_license_number(self):
        data = {"license_number": "1234ABC"}
        form = DriverLicenseUpdateForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_validate_license_number(self):
        license_number = "ABC12345"
        self.assertEqual(
            validate_license_number(license_number),
            license_number
        )

    def test_driver_license_update_form_valid_license_number(self):
        data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data)
        self.assertTrue(form.is_valid())

    def test_validate_license_number_invalid_length(self):
        license_number = "ABC1234"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)
