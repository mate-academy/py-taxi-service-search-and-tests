from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class TestForms(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "QWE12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TestValidationLicenseNumber(TestCase):
    def test_validation_when_len_of_license_number_more_than_8(self):
        with self.assertRaises(ValidationError) as error:
            validate_license_number("QWE12345678")

        self.assertEqual(
            str(error.exception),
            "['License number should consist of 8 characters']"
        )

    def test_validation_when_first_3_characters_are_not_upper_letters(self):
        with self.assertRaises(ValidationError) as error:
            validate_license_number("q1122345")

        self.assertEqual(
            str(error.exception),
            "['First 3 characters should be uppercase letters']"
        )

    def test_validation_when_last_5_characters_are_not_digits(
            self
    ):
        with self.assertRaises(ValidationError) as error:
            validate_license_number("QWERASDF")

        self.assertEqual(
            str(error.exception),
            "['Last 5 characters should be digits']"
        )
