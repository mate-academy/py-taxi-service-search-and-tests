from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class DriverCreationFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            "username": "user_one",
            "password1": "test123password",
            "password2": "test123password",
            "license_number": "AAA78945",
            "first_name": "Firstname",
            "last_name": "Lastname",
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_driver_creation_form_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_driver_creation_form_with_license_number_last_first_name(self):
        self.form.is_valid()
        self.assertEqual(self.form.cleaned_data, self.form_data)


class LicenseNumberValidationTest(TestCase):
    def test_valid_license_number(self):
        license_number = "QWE78945"
        self.assertEqual(
            validate_license_number(license_number),
            license_number
        )

    def test_invalid_format_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("invalid")

    def test_invalid_length_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("QWERT798")

    def test_invalid_first_three_characters_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("qwe45612")

    def test_invalid_last_five_characters_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("QWE123r4")
