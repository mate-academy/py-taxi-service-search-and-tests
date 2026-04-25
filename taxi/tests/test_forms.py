from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class TestDriverLicenseUpdateForm(TestCase):
    def test_driver_license_update_form_license_is_valid(self):
        license_number = "ABC12345"
        form = DriverLicenseUpdateForm(data={"license_number": license_number})
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_license_is_invalid(self):
        license_number = "nk1245"
        form = DriverLicenseUpdateForm(data={"license_number": license_number})
        self.assertFalse(form.is_valid())
