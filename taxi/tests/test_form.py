from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class LicenseNumberValidationFormTest(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_license_number_is_valid(self):
        self.assertTrue(self.create_form("ONE12345").is_valid())

    def test_length_of_license_number_not_less_than_8(self):
        self.assertFalse(self.create_form("ONE1234").is_valid())

    def test_length_of_license_number_not_more_than_8(self):
        self.assertFalse(self.create_form("ONE123456").is_valid())
