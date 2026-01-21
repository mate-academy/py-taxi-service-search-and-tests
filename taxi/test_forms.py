from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTests(TestCase):
    def test_license_number_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_number_invalid_length(self):
        form_data = {
            "username": "testuser",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
            "license_number": "AB1234",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_invalid_format(self):
        form_data = {
            "username": "testuser",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
            "license_number": "abc12345",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
