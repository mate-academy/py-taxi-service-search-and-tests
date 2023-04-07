from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import validate_license_number


class ValidateLicenseNumberTestCase(TestCase):
    def test_valid_license_number(self):
        license_number = "ABC12345"
        validated_license_number = validate_license_number(license_number)
        self.assertEqual(validated_license_number, license_number)

    def test_license_number_too_short(self):
        license_number = "ABC1234"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)

    def test_first_three_chars_not_uppercase_letters(self):
        license_number = "AbC12345"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)

    def test_last_five_chars_not_digits(self):
        license_number = "ABC1234X"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)
