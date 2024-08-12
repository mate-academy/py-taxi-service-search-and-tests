from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_create_form_valid_data(self):
        data = {
            "username": "user123",
            "password1": "79zilivi",
            "password2": "79zilivi",
            "first_name": "Ben",
            "last_name": "Adler",
            "license_number": "VVM45456",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_driver_create_form_invalid_data(self):
        data = {
            "username": "user123",
            "password1": "79zilivi",
            "password2": "79zilivi",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "is_missing",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
