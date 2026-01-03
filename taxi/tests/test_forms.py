from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm
)


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        driver = {
            "username": "iron_man1",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Tony",
            "last_name": "Stark",
            "license_number": "RGB98765"
        }
        form = DriverCreationForm(data=driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, driver)

    def test_license_update_form_valid_len_8symbols(self):
        license_number = {"license_number": "ABC1234567"}
        form = DriverLicenseUpdateForm(license_number)
        self.assertFalse(form.is_valid())

    def test_license_update_form_valid_first_3letters(self):
        license_number = {"license_number": "Abc12345"}
        form = DriverLicenseUpdateForm(license_number)
        self.assertFalse(form.is_valid())

    def test_license_update_form_valid_last_5digits(self):
        license_number = {"license_number": "ABC123c5"}
        form = DriverLicenseUpdateForm(license_number)
        self.assertFalse(form.is_valid())
