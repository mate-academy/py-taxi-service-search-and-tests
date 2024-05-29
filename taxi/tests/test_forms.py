from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
)


class FormsTests(TestCase):
    form_data_for_car = {
        "username": "test_driver",
        "password1": "pass1word123",
        "password2": "pass1word123",
        "license_number": "ABC12345",
        "first_name": "test_name",
        "last_name": "test_last_name",
    }

    def test_driver_creation_form_with_license_first_and_last_name(self):
        form = DriverCreationForm(data=self.form_data_for_car)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data_for_car)

    def test_invalid_license_number_during_creation_driver(self):
        self.form_data_for_car["license_number"] = "abc123"
        form = DriverCreationForm(data=self.form_data_for_car)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_invalid_license_number_during_updating_driver(self):
        form = DriverLicenseUpdateForm(data={"license_number": "12345678"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_invalid_license_number_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB12345")

    def test_invalid_license_number_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_invalid_license_number_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234A")
