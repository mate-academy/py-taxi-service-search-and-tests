from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import validate_license_number


class LicenseValidationTests(TestCase):
    def test_valid_license_number(self):
        result = validate_license_number("ABC12345")

        self.assertEqual(result, "ABC12345")

    def test_license_number_wrong_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_license_number_first_part_is_not_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_license_number_last_part_is_not_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12ABC")
