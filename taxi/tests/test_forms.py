from django.test import TestCase
from taxi.forms import DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_license_valid(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_invalid_lowercase(self):
        form_data = {"license_number": "abc12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_too_short(self):
        form_data = {"license_number": "AB123"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
