from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import validate_license_number


class LicenseNumberValidationTests(TestCase):
    def test_license_number_valid(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_must_have_eight_characters(self):
        with self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters",
        ):
            validate_license_number("ABC1234")

    def test_license_number_must_start_with_uppercase_letters(self):
        with self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters",
        ):
            validate_license_number("AbC12345")

    def test_license_number_must_end_with_digits(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Last 5 characters should be digits",
        ):
            validate_license_number("ABC1234D")
