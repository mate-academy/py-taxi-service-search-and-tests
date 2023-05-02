from unittest import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_correct(self):
        form_data = {
            "username": "ArlaCake",
            "password1": "somepassword123",
            "password2": "somepassword123",
            "first_name": "Arla",
            "last_name": "Cake",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_license_numbers(self):
        form_data = {
            "license_number": "67812345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_license_len_too_long(self):
        form_data = {
            "license_number": "ABC123456",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_license_lowercase_letters(self):
        form_data = {
            "license_number": "abc12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_license_letters_in_second_part(self):
        form_data = {
            "license_number": "ABC12A45",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
