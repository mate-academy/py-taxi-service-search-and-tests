from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverLicenseUpdateFormTest(TestCase):
    def test_if_license_number_not_meeting_length_param_too_short(self):
        """
        This test checking if license number consist 8 characters
        """
        form_data = {
            "username": "Test",
            "license_number": "TES1",
            "first_name": "Test",
            "last_name": "Test",
            "password1": "password123",
            "password2": "password123"
        }

        form = DriverCreationForm(data=form_data)

        self.assertRaises(ValidationError)
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "License number should consist of 8 characters"
        )

    def test_if_license_number_not_meeting_length_param_too_long(self):
        """
        This test checking if license number exceed 8 characters
        """
        form_data = {
            "username": "Test_new_driver",
            "license_number": "TES456789",
            "first_name": "Test",
            "last_name": "Test",
            "password1": "somewords123",
            "password2": "somewords123"
        }

        form = DriverCreationForm(data=form_data)

        self.assertRaises(ValidationError)
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "License number should consist of 8 characters"
        )

    def test_if_license_number_not_meeting_unique_param_numbers(self):
        """
        This test checking if last 5 characters
         at  end of license number  are numbers
        """
        form_data = {
            "username": "Test_new_driver",
            "license_number": "ABVc5678",
            "first_name": "Test",
            "last_name": "Test",
            "password1": "password123",
            "password2": "password123"
        }

        form = DriverCreationForm(data=form_data)

        self.assertRaises(ValidationError)
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "Last 5 characters should be digits"
        )

    def test_if_license_number_not_meeting_unique_param_letters(self):
        """
        This test checking if first 3 characters of license number
        are uppercase  letters
        """
        form_data = {
            "username": "Test_new_driver",
            "license_number": "AB345678",
            "first_name": "Test",
            "last_name": "Test",
            "password1": "password123",
            "password2": "password123"
        }

        form = DriverCreationForm(data=form_data)
        self.assertRaises(ValidationError)

        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "First 3 characters should be uppercase letters"
        )


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        """
        This test checking if driver creation form are valid
        """
        form_data = {
            "username": "test_user",
            "password1": "password123word",
            "password2": "password123word",
            "license_number": "ABV12345",
            "first_name": "test",
            "last_name": "test"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
