from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "password_test",
            "password2": "password_test",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validation_error_when_license_number_longer_then_eight(self):
        form_data = {
            "license_number": "ABC12345F"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_validation_error_when_license_number_first_three_characters_are_not_chars(self):
        form_data = {
            "license_number": "1BN12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_validation_error_when_license_number_first_three_characters_are_not_uppercase(self):
        form_data = {
            "license_number": "ABc12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_validation_error_when_license_number_where_last_five_characters_are_not_numbers(self):
        form_data = {
            "license_number": "ABN1234C"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
