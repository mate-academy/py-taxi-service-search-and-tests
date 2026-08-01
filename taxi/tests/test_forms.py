from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123",
            "password2": "user123",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "QWE12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_wrong_length(self):
        """Must be exactly 8 characters"""
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12"})
        self.assertFalse(form.is_valid())

    def test_license_number_first_three_not_uppercase(self):
        """First 3 characters must be uppercase letters"""
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})
        self.assertFalse(form.is_valid())

    def test_license_number_last_five_not_digits(self):
        """Last 5 characters must be digits"""
        form = DriverLicenseUpdateForm(data={"license_number": "ABCabcde"})
        self.assertFalse(form.is_valid())

    def test_license_number_valid(self):
        """Valid license number passes validation"""
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())
