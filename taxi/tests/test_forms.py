from django.test import TestCase
from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class LicenseNumberValidationTest(TestCase):
    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_invalid_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"],
        )

    def test_invalid_first_characters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"],
        )

    def test_invalid_last_characters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12X45"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"],
        )


class DriverCreateFormTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "Testusername",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "last_name": "last_name",
            "first_name": "first_name",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
