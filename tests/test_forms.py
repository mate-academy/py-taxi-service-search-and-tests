from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class FormTest(TestCase):
    def setUp(self):
        self.driver_data = {
            "username": "John123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345",
            "password1": "Jojoj123",
            "password2": "Jojoj123",
        }

    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(data=self.driver_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        invalid_data = self.driver_data.copy()
        invalid_data["license_number"] = "12345678"
        form = DriverCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_driver_validate_license_number_valid(self):
        correct_license_number = "ABC12345"
        try:
            validate_license_number(correct_license_number)
        except ValidationError:
            self.fail(
                "validate_license_number "
                "raised ValidationError unexpectedly!")
        self.assertTrue(validate_license_number(correct_license_number))

    def test_driver_validate_license_number_invalid(self):
        cases = [
            ("ABC1235", "License number should consist of 8 characters"),
            ("abc12345", "First 3 characters should be uppercase letters"),
            ("123ABCDE", "First 3 characters should be uppercase letters"),
            ("ABC1235A", "Last 5 characters should be digits"),
        ]
        for license_number, error_message in cases:
            with self.subTest(license=license_number):
                with self.assertRaises(ValidationError) as context:
                    validate_license_number(license_number)
                self.assertIn(error_message, str(context.exception))
