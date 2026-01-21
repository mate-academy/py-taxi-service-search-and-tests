
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
)


class DriverFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "XYZ12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "abc123",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
