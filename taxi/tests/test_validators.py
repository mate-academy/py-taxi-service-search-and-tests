import unittest
from django.core.exceptions import ValidationError
from taxi.forms import validate_license_number


class ValidateLicenseNumberTest(unittest.TestCase):

    def test_valid_license_number(self):
        result = validate_license_number("ASD12345")
        self.assertEqual(result, "ASD12345")

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ASD1234")

    def test_invalid_prefix(self):
        with self.assertRaises(ValidationError):
            validate_license_number("asd12345")

    def test_invalid_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ASD1234A")
