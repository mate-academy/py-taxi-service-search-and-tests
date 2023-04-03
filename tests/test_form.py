from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class TestForm(TestCase):
    def test_driver_creation_form(self):
        data = {
            "username": "fast",
            "password1": "fast1password",
            "password2": "fast1password",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_driver_update_form_with_correct_data(self):
        data = {"license_number": "ASD12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_license_number(), "ASD12345")

    def test_driver_update_form_with_not_3_first_uppercase_letter(self):
        data = {"license_number": "AD12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_update_form_with_not_5_last_digit(self):
        data = {"license_number": "FOUr2345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_update_form_with_not_8_characters(self):
        data = {"license_number": "FOUr12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
