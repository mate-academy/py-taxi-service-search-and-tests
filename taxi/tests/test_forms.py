from django.test import TestCase
from taxi.forms import validate_license_number, DriverCreationForm
from django.core.exceptions import ValidationError


class LicenseNumberValidationTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(
            validate_license_number("ABC12345"),
            "ABC12345"
        )

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")

    def test_invalid_first_part(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_invalid_last_part(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12A45")


class DriverCreationFormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "username": "driver1",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_license(self):
        form_data = {
            "username": "driver1",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "abc123",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
