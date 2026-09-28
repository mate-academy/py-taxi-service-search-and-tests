from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
)


class LicenseNumberValidationTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_must_contain_eight_characters(self):
        with self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters",
        ):
            validate_license_number("ABC1234")

    def test_first_three_characters_must_be_uppercase_letters(self):
        with self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters",
        ):
            validate_license_number("AbC12345")

    def test_last_five_characters_must_be_digits(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Last 5 characters should be digits",
        ):
            validate_license_number("ABC12D45")


class DriverCreationFormTest(TestCase):
    def test_license_number_validation_is_used_by_creation_form(self):
        form = DriverCreationForm(
            data={
                "username": "alex",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "license_number": "ABC1234",
                "first_name": "Alex",
                "last_name": "Smith",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"],
        )


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_number_validation_is_used_by_update_form(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12D45"})

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"],
        )
