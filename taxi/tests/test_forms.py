from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "pass123word",
            "password2": "pass123word",
            "first_name": "first",
            "last_name": "last",
            "license_number": "AMD12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_is_valid(self):
        form_data = {"license_number": "AMD12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_is_not_valid_length(self):
        form_data = {"license_number": "AMD1234"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_is_not_valid_letters(self):
        form_data = {"license_number": "AMd12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_is_not_valid_digits(self):
        form_data = {"license_number": "AMD12AMD"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
