from django.test import TestCase
from django.core.exceptions import ValidationError

from taxi.forms import validate_license_number


class FormValidationTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_wrong_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB123")

        with self.assertRaises(ValidationError):
            validate_license_number("ABC123456")

    def test_license_number_first_three_not_uppercase_alpha(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

        with self.assertRaises(ValidationError):
            validate_license_number("12A12345")

    def test_license_number_last_five_not_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234A")
