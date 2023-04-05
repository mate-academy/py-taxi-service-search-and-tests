from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms_logic import validate_license_number


class TestLicenseNumberValidation(TestCase):
    def test_valid_license_number(self):
        license_number = "ABC12345"

        self.assertEqual(
            validate_license_number(license_number), license_number
        )

    def test_license_number_has_no_exact_length(self):
        license_number = "ABC123456"

        with self.assertRaisesMessage(
            ValidationError, "License number should consist of 8 characters"
        ):
            validate_license_number(license_number)

    def test_license_number_wrong_first_tree_letters(self):
        wrong_license_numbers = [
            "aBC12345",
            "AbC12345",
            "ABc12345",
            "abc12345",
        ]

        for license_number in wrong_license_numbers:
            with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters",
            ):
                validate_license_number(license_number)

    def test_license_number_wrong_last_five_characters(self):
        wrong_license_numbers = [
            "ABCs2345",
            "ABC1d345",
            "ABC12!45",
            "ABC123&5",
            "ABC1234 ",
        ]

        for license_number in wrong_license_numbers:
            with self.assertRaisesMessage(
                ValidationError, "Last 5 characters should be digits"
            ):
                validate_license_number(license_number)
