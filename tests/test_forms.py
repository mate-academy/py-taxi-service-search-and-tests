from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number
)


class FormTests(TestCase):
    def test_driver_creation_form_with_custom_fields(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_invalid_license_number(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "a2CNM123",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "XYZ98765"
        }
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_invalid(self):
        form_data = {
            "license_number": "987ABCXYZ"
        }
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_validate_license_number_len_greater_8(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC123456")
        self.assertEqual(
            context.exception.message,
            "License number should consist of 8 characters"
        )

    def test_validate_license_number_fist_three_ch_not_upper_or_letters(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("abc12345")
        self.assertEqual(
            context.exception.message,
            "First 3 characters should be uppercase letters"
        )

    def test_validate_license_number_last_five_characters_are_not_digits(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC1234B")
        self.assertEqual(
            context.exception.message, "Last 5 characters should be digits"
        )
