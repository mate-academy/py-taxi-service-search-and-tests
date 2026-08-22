from django.test import TestCase
from taxi.forms import DriverLicenseUpdateForm


class DriverLicenseFormTests(TestCase):
    def test_driver_license_number_valid_format(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_number_invalid_if_not_8_chars(self):
        form_data = {"license_number": "ABC1234"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_invalid_first_three_not_uppercase(self):
        form_data = {"license_number": "abc12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_invalid_last_five_not_digits(self):
        form_data = {"license_number": "ABC1234X"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
