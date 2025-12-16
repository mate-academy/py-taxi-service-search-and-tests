from django.test import TestCase
from django.core.exceptions import ValidationError
from taxi.forms import validate_license_number


class LicenseValidationTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(
            validate_license_number("ABC12345"), "ABC12345"
        )

    def test_invalid_length(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number("ABC1234")

    def test_invalid_first_three_chars(self):
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("AbC12345")

    def test_invalid_last_five_chars(self):
        with self.assertRaisesMessage(
                ValidationError, "Last 5 characters should be digits"
        ):
            validate_license_number("ABC12X45")
