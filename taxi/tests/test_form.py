from django.test import TestCase
from taxi.forms import DriverLicenseUpdateForm


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_form(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"license_number": "12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
