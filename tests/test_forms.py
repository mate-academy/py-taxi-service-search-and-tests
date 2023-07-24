from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creat_with_license_number_first_and_last_name(self):
        form_data = {
            "username": "nova",
            "password1": "nova123456",
            "password2": "nova123456",
            "license_number": "ASD12345",
            "first_name": "Sarah",
            "last_name": "Kerigan",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_validate_license_number_with_8_characters(self):
        form_data = {
            "username": "nova",
            "password1": "nova123456",
            "password2": "nova123456",
            "license_number": "AD12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_validate_license_number_with_first_3_uppercase_letters(self):
        form_data = {
            "username": "nova",
            "password1": "nova123456",
            "password2": "nova123456",
            "license_number": "AdS12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_validate_license_number_with_last_5_digits(self):
        form_data = {
            "username": "nova",
            "password1": "nova123456",
            "password2": "nova123456",
            "license_number": "ADS1234q",
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )
