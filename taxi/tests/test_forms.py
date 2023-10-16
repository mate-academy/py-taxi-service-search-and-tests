from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user_password",
            "password2": "user_password",
            "first_name": "Name1",
            "last_name": "Name2",
            "license_number": "ASF45342",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTestCase(TestCase):

    def test_valid_license_number(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self):
        invalid_license_numbers = ["1234", "AB", "ABC-123"]
        for license_number in invalid_license_numbers:
            form_data = {"license_number": license_number}
            form = DriverLicenseUpdateForm(data=form_data)
            self.assertFalse(form.is_valid())

    def test_empty_license_number(self):
        form_data = {"license_number": ""}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
