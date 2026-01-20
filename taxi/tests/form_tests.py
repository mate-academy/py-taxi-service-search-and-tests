from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class FormTestClass(TestCase):
    def test_license_number_is_invalid_when_too_short(self):
        data = {"license_number": "abc"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertEqual(
            form.errors["license_number"][0],
            "License number should consist of 8 characters"
        )

    def test_license_number_is_invalid_when_all_letters(self):
        data = {"license_number": "ABCDEFGH"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertEqual(
            form.errors["license_number"][0],
            "Last 5 characters should be digits"
        )

    def test_license_number_is_invalid_when_digits_first(self):
        data = {"license_number": "123DEFGH"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertEqual(
            form.errors["license_number"][0],
            "First 3 characters should be uppercase letters"
        )

    def test_license_number_is_valid(self):
        data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())
