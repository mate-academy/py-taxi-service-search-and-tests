from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_creation_form_with_lowercase_letters(self):
        test_data = {
            "username": "test",
            "license_number": "qwe12345",
            "password1": "password1234567",
            "password2": "password1234567",
        }

        form = DriverCreationForm(data=test_data)

        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_incorrect_license_number_length(self):
        test_data = {
            "username": "test",
            "license_number": "qwe12345",
            "password1": "password1234567",
            "password2": "password1234567",
        }

        form = DriverCreationForm(data=test_data)

        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_only_1_letter(self):
        test_data = {
            "username": "test",
            "license_number": "Q1111111",
            "password1": "password1234567",
            "password2": "password1234567",
        }

        form = DriverCreationForm(data=test_data)

        self.assertFalse(form.is_valid())

    def test_driver_update_license_form(self):

        test_data = {
            "license_number": "GGG33333"
        }

        form = DriverLicenseUpdateForm(data=test_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test_data)
