from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class DriverLicenceFormTest(TestCase):

    def test_licence_valid(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_licence_invalid_length(self):
        form_data = {
            "license_number": "ABC123453",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_licence_invalid_first_latters(self):
        form_data = {
            "license_number": "ABc12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_licence_invalid_last_digits(self):
        form_data = {
            "license_number": "ABC12a45",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
