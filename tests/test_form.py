from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class LicenseUpdateTestCase(TestCase):
    def test_license_update_is_valid(self):
        form_data = {
            "license_number": "ABC12345",
        }
        license_num = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(license_num.is_valid(), True)

    def test_license_update_not_is_valid(self):
        form_data = {
            "license_number": "ABC",
        }
        license_num = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(license_num.is_valid(), False)
