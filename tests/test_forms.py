from django.test import TestCase
from django.core.exceptions import ValidationError

from taxi.forms import (
    validate_license_number,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)


class FormsTests(TestCase):
    def test_validate_license_number_valid(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_validate_license_number_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")

    def test_validate_license_number_first_3_not_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_validate_license_number_last_5_not_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABCabcde")

    def test_driver_creation_form_with_valid_data(self):
        form = DriverCreationForm(
            data={
                "username": "test_driver",
                "password1": "test_password123",
                "password2": "test_password123",
                "first_name": "John",
                "last_name": "Doe",
                "license_number": "ABC12345",
            }
        )

        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_with_valid_data(self):
        form = DriverLicenseUpdateForm(
            data={
                "license_number": "ABC12345",
            }
        )

        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_with_invalid_data(self):
        form = DriverLicenseUpdateForm(
            data={
                "license_number": "abc12345",
            }
        )

        self.assertFalse(form.is_valid())
