from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import validate_license_number


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        result = validate_license_number("GDF12345")
        self.assertEqual(result, "GDF12345")

    def test_invalid_license_number_too_short(self):
        with self.assertRaises(ValidationError):
            validate_license_number("GDF1234")

    def test_invalid_license_number_too_long(self):
        with self.assertRaises(ValidationError):
            validate_license_number("GDF123456")

    def test_invalid_license_number_capital_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("des12345")

    def test_invalid_license_number_first_three_symbols_not_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("G1F12345")

    def test_invalid_license_number_last_five_symbols_not_numbers(self):
        with self.assertRaises(ValidationError):
            validate_license_number("G1F1234A")
