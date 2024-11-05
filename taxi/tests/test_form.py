from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "testuser",
            "password1": "testpa10-ssworD",
            "password2": "testpa10-ssworD",
            "first_name": "First",
            "last_name": "Second",
            "license_number": "ADF12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTests(TestCase):
    def test_license_number_update_form_with_valid_information(self):
        form_data = {
            "license_number": "ADF12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_update_form_with_invalid_information(self):
        form_data = {
            "license_number": "AD112345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {
            "license_number": "ADf12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {
            "license_number": "ADFD2345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {
            "license_number": "ADF234566",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
