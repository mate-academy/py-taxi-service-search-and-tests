from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from taxi.forms import (
    validate_license_number,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)


class ValidateLicenseNumberTest(SimpleTestCase):
    def test_license_number_has_more_than_eight_characters(self):
        with self.assertRaisesMessage(
            ValidationError, "License number should consist of 8 characters"
        ):
            validate_license_number("ABC123456")

    def test_license_number_has_less_than_eight_characters(self):
        with self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters",
        ):
            validate_license_number("ABC1234")

    def test_first_three_characters_are_not_uppercase(self):
        with self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters",
        ):
            validate_license_number("AbC12345")

    def test_first_three_characters_contain_digit(self):
        with self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters",
        ):
            validate_license_number("A1C12345")

    def test_fourth_character_is_letter(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Last 5 characters should be digits",
        ):
            validate_license_number("ABCD1234")

    def test_valid_license_number(self):
        result = validate_license_number("ABC12345")

        self.assertEqual(result, "ABC12345")


class DriverCreationFormTests(TestCase):
    def test_form_rejects_invalid_license_number(self):
        form = DriverCreationForm(
            data={
                "username": "test_driver",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "abc12345",
                "first_name": "John",
                "last_name": "Smith",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"],
        )

    def test_form_accepts_valid_license_number(self):
        form = DriverCreationForm(
            data={
                "username": "test_driver",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "ABC12345",
                "first_name": "John",
                "last_name": "Smith",
            }
        )

        self.assertTrue(form.is_valid())


class DriverLicenseUpdateFormTests(TestCase):
    def test_form_rejects_invalid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABCD1234"})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"],
        )

    def test_form_accepts_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})

        self.assertTrue(form.is_valid())
