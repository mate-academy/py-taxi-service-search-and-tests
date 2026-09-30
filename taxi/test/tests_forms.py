from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_number_is_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_license_number_with_invalid_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234"})
        self.assertFalse(form.is_valid())

    def test_license_number_with_lowercase_letters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "aBC12345"})
        self.assertFalse(form.is_valid())

    def test_license_number_with_non_digit_suffix(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234X"})
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_form_with_valid_license_number_is_valid(self):
        form = DriverCreationForm(
            data={
                "username": "test",
                "password1": "TestPassword123",
                "password2": "TestPassword123",
                "license_number": "ABC12345",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_license_number_is_invalid(self):
        form = DriverCreationForm(
            data={
                "username": "test",
                "password1": "TestPassword123",
                "password2": "TestPassword123",
                "license_number": "ABC12x45",
            }
        )
        self.assertFalse(form.is_valid())
