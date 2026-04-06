from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverTestForms(TestCase):
    def test_driver_creation_form_with_valid_license(self):
        form_data = {
            "username": "test",
            "license_number": "ABC12345",
            "first_name": "First Test",
            "last_name": "Last Test",
            "password1": "test123Strong",
            "password2": "test123Strong",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_with_invalid_license(self):
        form_data = {
            "username": "test",
            "license_number": "abd12345",
            "first_name": "First Test",
            "last_name": "Last Test",
            "password1": "test123Strong",
            "password2": "test123Strong",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_update_license_form_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ab12345"})
        self.assertFalse(form.is_valid())

    def test_driver_update_license_form_first_3_upper(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "abc12345"}
        )
        self.assertFalse(form.is_valid())

    def test_driver_update_license_form_first_3_digit(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "1bc12345"}
        )
        self.assertFalse(form.is_valid())

    def test_driver_update_license_form_last_5_digit(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC123aa"}
        )
        self.assertFalse(form.is_valid())

    def test_driver_update_license_form_valid(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"}
        )
        self.assertTrue(form.is_valid())
