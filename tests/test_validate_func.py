from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import validate_license_number


class ValidateLicenseNumberTest(TestCase):
    def test_validate_license_number_if_is_valid(self) -> None:
        self.assertEqual(validate_license_number("AAA12345"), "AAA12345")

    def test_validate_license_number_length_not_equal_eight(self) -> None:
        self.assertRaisesRegex(
            ValidationError,
            "License number should consist of 8 characters",
            validate_license_number,
            "AAA1234",
        )

    def test_validate_license_number_length_first_three_character_is_not_upper(self) -> None:
        self.assertRaisesRegex(
            ValidationError,
            "First 3 characters should be uppercase letters",
            validate_license_number,
            "abc12345",
        )

    def test_validate_license_number_length_last_five_character_must_be_digits(self) -> None:
        self.assertRaisesRegex(
            ValidationError,
            "Last 5 characters should be digits",
            validate_license_number,
            "ABC1ff45",
        )