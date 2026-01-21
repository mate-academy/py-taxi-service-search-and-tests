from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_creation_form_with_lowercase_letters(self):
        test_data = {
            "username": "test",
            "license_number": "aaa00000",
            "password1": "thisistestpassword123456789",
            "password2": "thisistestpassword123456789",
        }

        form = DriverCreationForm(data=test_data)

        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_incorrect_license_number_length(self):
        test_data = {
            "username": "test",
            "license_number": "AAA000000",
            "password1": "thisistestpassword123456789",
            "password2": "thisistestpassword123456789",
        }

        form = DriverCreationForm(data=test_data)

        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_only_1_letter(self):
        test_data = {
            "username": "test",
            "license_number": "A0000000",
            "password1": "thisistestpassword123456789",
            "password2": "thisistestpassword123456789",
        }

        form = DriverCreationForm(data=test_data)

        self.assertFalse(form.is_valid())

    def test_driver_update_license_form(self):

        test_data = {
            "license_number": "BBB22222"
        }

        form = DriverLicenseUpdateForm(data=test_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test_data)
