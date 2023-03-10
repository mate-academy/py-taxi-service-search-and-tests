from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    validate_license_number,
    DriverLicenseUpdateForm
)


class FormTests(TestCase):
    def test_driver_creation_form_is_valid(self) -> None:
        form_data = {
            "username": "test_username",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12346",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_license_number_form_is_valid(self) -> None:
        form_data = {
            "license_number": "TES12346",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_number_with_incorrect_length(self):
        message = "License number should consist of 8 characters"
        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number("TES1234")

    def test_validate_license_number_with_incorrect_first_3_characters(self):
        message = "First 3 characters should be uppercase letters"
        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number("tES12345")

    def test_validate_license_number_with_incorrect_last_5_digits(self):
        message = "Last 5 characters should be digits"
        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number("TES1234t")
