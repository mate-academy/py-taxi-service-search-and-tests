from django.test import TestCase
from django.core.exceptions import ValidationError

from taxi.forms import validate_license_number


class FormsTests(TestCase):
    def test_validate_license_number_valid(self):
        valid_license = "ABC12345"
        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_validate_license_number_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_validate_license_number_invalid_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("123ABCDE")

    def test_validate_license_number_invalid_numbers(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABCDEFGH")
