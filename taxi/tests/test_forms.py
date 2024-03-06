from django.test import TestCase
from django.forms import ValidationError
from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        validate_license_number)


class DriverFormsTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "differentpassword",
            "license_number": "invalid_license",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_driver_license_update_form_valid(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {"license_number": "invalid_license"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_validate_license_number_valid(self):
        valid_license_numbers = ["ABC12345", "XYZ67890"]
        for license_number in valid_license_numbers:
            self.assertEqual(
                validate_license_number(license_number),
                license_number
            )

    def test_validate_license_number_invalid(self):
        invalid_license_numbers = ["invalid", "12345", "ABCD1234", "ABC123456"]
        for license_number in invalid_license_numbers:
            with self.assertRaises(ValidationError):
                validate_license_number(license_number)
