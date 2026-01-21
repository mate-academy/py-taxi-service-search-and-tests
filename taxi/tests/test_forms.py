from taxi.forms import DriverLicenseUpdateForm

from django.test import TestCase


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_invalid_license_number_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234"})
        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_invalid_license_number_uppercase(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_invalid_license_number_letters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AB112345"})
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_invalid_license_number_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12A45"})
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )
