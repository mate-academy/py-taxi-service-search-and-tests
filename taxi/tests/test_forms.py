from django.test import TestCase
from django.core.exceptions import ValidationError

from taxi.forms import (
    validate_license_number,
    DriverLicenseUpdateForm,
    DriverCreationForm,
)


class ValidateLicenseNumberTest(TestCase):
    def test_validate_license_number_with_valid_data(self):
        license_number = "ABC12345"
        self.assertEqual(
            validate_license_number(license_number),
            license_number
        )

    def test_validate_license_number_with_invalid_length(self):
        license_number = "1234AB"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)

    def test_validate_license_number_with_invalid_first_three_characters(self):
        license_number = "abc12345"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)

    def test_validate_license_number_with_invalid_last_five_characters(self):
        license_number = "ABC1234a"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)


class DriverLicenseUpdateFormTests(TestCase):
    def test_driver_license_update_form_with_valid_license_number(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_with_invalid_license_number(self):
        form_data = {"license_number": "abc12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverCreationFormTest(TestCase):
    def setUp(self):
        self.form_data_valid = {
            "username": "test_driver",
            "password1": "test_password_123",
            "password2": "test_password_123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Smith",
        }

    def test_driver_creation_form_with_valid_license_number(self):
        form_valid = DriverCreationForm(data=self.form_data_valid)
        self.assertTrue(form_valid.is_valid())

    def test_driver_creation_form_with_invalid_license_number(self):
        form_data_invalid = self.form_data_valid.copy()
        form_data_invalid["license_number"] = "abc12345"

        form_invalid = DriverCreationForm(data=form_data_invalid)

        self.assertFalse(form_invalid.is_valid())
        self.assertIn("license_number", form_invalid.errors)
