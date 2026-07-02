from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class TestForms(TestCase):
    def test_driver_update_license_number_is_too_short(self):
        form = DriverLicenseUpdateForm(data={"license_number": "12345"})
        self.assertFalse(form.is_valid())

    def test_driver_update_license_number_first_chars_are_lowercase(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})
        self.assertFalse(form.is_valid())

    def test_driver_update_license_number_first_three_chars_are_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "12312345"})
        self.assertFalse(form.is_valid())

    def test_driver_update_license_number_last_five_chars_are_not_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABCQWERTY"})
        self.assertFalse(form.is_valid())

    def test_driver_update_valid_form(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())
