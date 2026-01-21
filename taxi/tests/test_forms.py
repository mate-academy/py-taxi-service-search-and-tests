from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class LicenseUpdateTest(TestCase):

    def test_invalid_uppercase(self):
        form_data = {
            "license_number": "abc12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_digits_and_letters_number(self):
        form_data = {
            "license_number": "ABCD2345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_length(self):
        form_data = {
            "license_number": "ABC12345678"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_chars_placement(self):
        form_data = {
            "license_number": "12345ABC"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_license_number(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )


class DriverCreationFormTest(TestCase):

    def test_user_creation_and_validation(self):
        form_data = {
            "username": "testuser",
            "password1": "aabbcc123321",
            "password2": "aabbcc123321",
            "first_name": "test",
            "last_name": "user",
            "license_number": "ABC12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
