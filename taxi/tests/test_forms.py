from django import test
from django.core.exceptions import ValidationError

from taxi.forms import validate_license_number


class TestValidateLicenseValidator(test.TestCase):
    def test_valid_data(self):
        license_number = "ABC12345"
        self.assertEqual(
            validate_license_number(license_number),
            license_number
        )

    def test_short_or_long_data(self):
        license_number1 = "ABC123455"
        license_number2 = "ABC1234"
        with self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters"
        ):
            validate_license_number(license_number1),
        with self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters"
        ):
            validate_license_number(license_number2),

    def test_invalid_first_3_characters(self):
        license_number1 = "ABc12345"
        with self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters"
        ):
            validate_license_number(license_number1)

    def test_invalid_last_5_characters(self):
        license_number1 = "ABCD2345"
        with self.assertRaisesMessage(
            ValidationError,
            "Last 5 characters should be digits"
        ):
            validate_license_number(license_number1)
