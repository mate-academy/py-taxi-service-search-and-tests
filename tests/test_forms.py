from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_valid_data(self):
        form_data = {
            "username": "wickjohn",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "jonh",
            "last_name": "wick",
            "license_number": "JWL12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_invalid_data(self):
        form_data = {
            "username": "wickjohn",
            "password1": "test123",
            "password2": "test321",
            "first_name": "",
            "last_name": "",
            "license_number": "short"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertIn("license_number", form.errors)
