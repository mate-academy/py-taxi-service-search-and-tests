from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_validation_license_short(self):
        form_data = {
            "username": "Test_new_driver",
            "license_number": "TES",
            "first_name": "Test name",
            "last_name": "Test surname",
            "password1": "smthlike123",
            "password2": "smthlike123"
        }

        form = DriverCreationForm(data=form_data)

        self.assertRaises(ValidationError)
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "License number should consist of 8 characters"
        )

    def test_driver_validation_license_long(self):
        form_data = {
            "username": "Test_new_driver",
            "license_number": "TES456789",
            "first_name": "Test name",
            "last_name": "Test surname",
            "password1": "smthlike123",
            "password2": "smthlike123"
        }

        form = DriverCreationForm(data=form_data)

        self.assertRaises(ValidationError)
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "License number should consist of 8 characters"
        )

    def test_driver_validation_license_not_enough_numbers(self):
        form_data = {
            "username": "Test_new_driver",
            "license_number": "TESt5678",
            "first_name": "Test name",
            "last_name": "Test surname",
            "password1": "smthlike123",
            "password2": "smthlike123"
        }

        form = DriverCreationForm(data=form_data)

        self.assertRaises(ValidationError)
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "Last 5 characters should be digits"
        )

    def test_driver_validation_license_not_enough_letters(self):
        form_data = {
            "username": "Test_new_driver",
            "license_number": "TE345678",
            "first_name": "Test name",
            "last_name": "Test surname",
            "password1": "smthlike123",
            "password2": "smthlike123"
        }

        form = DriverCreationForm(data=form_data)
        self.assertRaises(ValidationError)

        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "First 3 characters should be uppercase letters"
        )


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "password123egege",
            "password2": "password123egege",
            "license_number": "SET87654",
            "first_name": "test first name",
            "last_name": "test last name"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
