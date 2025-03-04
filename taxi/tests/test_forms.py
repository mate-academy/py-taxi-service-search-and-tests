from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class FormTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        data = {
            "username": "User",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "license_number": "BBB22222",
            "first_name": "user first",
            "last_name": "user last"
        }

        form = DriverCreationForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)


class ValidateLicenseNumberTests(TestCase):
    def test_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("VVV111111")
        with self.assertRaises(ValidationError):
            validate_license_number("VVV")
        self.assertEqual(validate_license_number("AAA11111"), "AAA11111")

    def test_first_three_char(self):
        with self.assertRaises(ValidationError):
            validate_license_number("VV1111111")
        with self.assertRaises(ValidationError):
            validate_license_number("vVV11111")
        self.assertEqual(validate_license_number("VVV11111"), "VVV11111")

    def test_last_five_num(self):
        with self.assertRaises(ValidationError):
            validate_license_number("VVV111v1")
