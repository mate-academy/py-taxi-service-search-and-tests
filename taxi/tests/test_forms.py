from django.test import TestCase
from django.core.exceptions import ValidationError
from taxi.forms import validate_license_number


class FormValidationTest(TestCase):

    def test_valid_license_number(self):
        valid_license = "ABC12345"
        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_license_number_wrong_length(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("AB1234")
        self.assertEqual(
            context.exception.message,
            "License number should consist of 8 characters"
        )

    def test_license_number_first_3_not_uppercase_letters(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("abC12345")
        self.assertEqual(
            context.exception.message,
            "First 3 characters should be uppercase letters"
        )

    def test_license_number_last_5_not_digits(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC1234X")
        self.assertEqual(
            context.exception.message,
            "Last 5 characters should be digits"
        )
