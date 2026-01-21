from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import validate_license_number, DriverLicenseUpdateForm


class FormsTest(TestCase):
    def test_license_validation_with_short_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("12345")

    def test_license_validation_with_long_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12345678")

    def test_license_validation_with_no_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("12312345")

    def test_license_validation_with_no_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ZXCQWERTY")

    def test_license_validation_with_valid_data(self):
        self.assertTrue(validate_license_number("ABC12345"))

    def test_license_number_update_form_valid(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_number_update_form_invalid(self):
        form_data = {
            "license_number": "ABC123",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
