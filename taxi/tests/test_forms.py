from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class DriverCreationFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "user55test",
            "password2": "user55test",
            "license_number": "ABC12345",
            "first_name": "First user",
            "last_name": "Last user",
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_driver_creation_form_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_driver_creation_form_with_license_number_last_first_name(self):
        self.form.is_valid()
        self.assertEqual(self.form.cleaned_data, self.form_data)


class LicenseNumberValidationTest(TestCase):
    def test_valid_license_number(self):
        license_number = "ABC12345"
        self.assertEqual(
            validate_license_number(license_number),
            license_number
        )

    def test_invalid_format_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("invalid")

    def test_invalid_length_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABCDE123")

    def test_invalid_first_three_characters_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_invalid_last_five_characters_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12a45")
