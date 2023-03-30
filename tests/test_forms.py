from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_form_with_additional_parameters(self):
        form_data = {
            "username": "OrdinaryUser",
            "password1": "12121212@A",
            "password2": "12121212@A",
            "first_name": "Ordinary",
            "last_name": "User",
            "license_number": "ABC12346"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_invalid_license_number(self):
        invalid_licence_numbers = [
            "ABC1234",
            "BC12346",
            "12345678",
            "ABCDEFGH",
            "aBC12346",
            "ABC1234q"
        ]
        for licence_number in invalid_licence_numbers:
            form_data = {
                "username": "OrdinaryUser",
                "password1": "12121212@A",
                "password2": "12121212@A",
                "first_name": "Ordinary",
                "last_name": "User",
                "license_number": licence_number
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertNotEqual(form.cleaned_data, form_data)
