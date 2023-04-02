from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_driver_license_valid_input(self) -> None:
        form_data = {
            "username": "Testill",
            "first_name": "Test",
            "last_name": "Testovich",
            "password1": "pastest456",
            "password2": "pastest456",
            "license_number": "ATB12345",
        }
        form = DriverCreationForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_invalid_input(self) -> None:
        form_data = {
            "username": "Testill",
            "first_name": "Test",
            "last_name": "Testovich",
            "password1": "pastest456",
            "password2": "pastest456",
        }

        license_numbers = [" ", "yt23727", "TY567777", "********", "GHTghghgh", "1", "ATB6765T"]

        for license_num in license_numbers:
            form_data["license_number"] = license_num
            form = DriverCreationForm(form_data)
            self.assertFalse(form.is_valid())
