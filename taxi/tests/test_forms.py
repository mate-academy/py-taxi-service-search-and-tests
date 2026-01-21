from django.core.exceptions import ValidationError
from django.test import TestCase
from taxi.forms import DriverCreationForm, validate_license_number


class FormsCreateDriverTests(TestCase):
    def test_create_driver_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user11test",
            "password2": "user11test",
            "license_number": "ABC12345",
            "first_name": "new first",
            "last_name": "new last",
        }
        form = DriverCreationForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class ValidateLicenseNumberTests(TestCase):
    def test_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123456")

    def test_first_three_upper_case(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abC12345")

    def test_last_five_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1A345")

    def test_valid_license_number(self):
        result = validate_license_number("ABC12345")
        self.assertEqual(result, "ABC12345")
