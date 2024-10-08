from django.test import TestCase
from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid_data(self):
        """Test that form accepts valid data."""
        form_data = {
            "username": "testdriver",
            "password1": "StrongPassw0rd!",
            "password2": "StrongPassw0rd!",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_data(self):
        """Test that form rejects invalid license number."""
        form_data = {
            "username": "testdriver",
            "password1": "StrongPassw0rd!",
            "password2": "StrongPassw0rd!",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "invalid"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
