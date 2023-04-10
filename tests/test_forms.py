from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number
)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "miwa_dr",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Miwa",
            "last_name": "Vovchok",
            "license_number": "NNN78555",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_not_valid(self):
        form_data = {
            "username": "driver",
            "password1": "fdbgfdbx",
            "password2": "fdbgfdbx",
            "license_number": "",
            "first_name": "",
            "last_name": "",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_update_form_valid(self):
        driver = get_user_model().objects.create(username="driver")
        form = DriverLicenseUpdateForm(
            data={"license_number": "MVO45896"},
            instance=driver
        )
        self.assertTrue(form.is_valid())

    def test_license_update_form_invalid(self):
        driver = get_user_model().objects.create(username="driver")
        form = DriverLicenseUpdateForm(
            data={"license_number": "5VO45N96"},
            instance=driver
        )
        self.assertFalse(form.is_valid())

    def test_validate_license_number_last_five_characters_are_not_digits(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC1234B")
        self.assertEqual(
            context.exception.message, "Last 5 characters should be digits"
        )

    def test_validate_license_number_first_three_char_should_be_Ltrs(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("A8C12345")
        self.assertEqual(
            context.exception.message, "First 3 characters should be letters"
        )

    def test_validate_license_number_fist_three_characters_not_upper(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("abc12345")
        self.assertEqual(
            context.exception.message,
            "First 3 characters should be uppercase letters"
        )
