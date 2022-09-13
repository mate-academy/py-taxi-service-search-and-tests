from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class DriverFormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class ValidLicenseNumberTests(TestCase):
    def test_correct_license_number(self):
        license_number = "TES12345"

        self.assertEqual(validate_license_number(license_number), license_number)

    def test_length_of_license_number_is_bigger_than_8(self):
        license_number = "TES123456"
        message = "License number should consist of 8 characters"

        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number(license_number)

    def test_length_of_license_number_is_less_than_8(self):
        license_number = "TES1234"
        message = "License number should consist of 8 characters"

        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number(license_number)

    def test_first_3_characters_should_be_uppercase_letters(self):
        license_number = "TE123456"
        message = "First 3 characters should be uppercase letters"

        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number(license_number)

    def test_last_5_characters_should_be_digits(self):
        license_number = "TESTTEST"
        message = "Last 5 characters should be digits"

        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number(license_number)
