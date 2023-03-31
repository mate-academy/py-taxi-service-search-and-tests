from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_creation_with_fields_is_valid(self):
        form_data = {
            "username": "Username",
            "password1": "Pass123-wrd",
            "password2": "Pass123-wrd",
            "first_name": "First Name",
            "last_name": "Last Name",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_update_form_with_wrong_length(self):
        form_data = {
            "license_number": "AANK84812"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_license_number_update_form_with_lower_letters(self):
        form_data = {
            "license_number": "AnK84812"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_license_number_update_form_with_less_numbers(self):
        form_data = {
            "license_number": "ANKK4812"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_license_number_update_form_with_more_numbers(self):
        form_data = {
            "license_number": "AN674812"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
