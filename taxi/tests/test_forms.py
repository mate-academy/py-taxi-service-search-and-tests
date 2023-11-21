from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_fisrt_and_last_name(self):
        form_data = {
            "username": "test",
            "password1": "usertest",
            "password2": "usertest",
            "first_name": "testname",
            "last_name": "testlast",
            "license_number": "ASD12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_length(self):
        license_number = "ASD1234"
        with self.assertRaises(ValidationError) as excep:
            validate_license_number(license_number)
        self.assertEqual(
            str(excep.exception),
            "['License number should consist of 8 characters']"
        )

    def test_license_number_first_letters(self):
        license_number = "asd12345"
        with self.assertRaises(ValidationError) as excep:
            validate_license_number(license_number)
        self.assertEqual(
            str(excep.exception),
            "['First 3 characters should be uppercase letters']"
        )

    def test_license_number_five_last_numbers(self):
        license_number = "ASD12#$%"
        with self.assertRaises(ValidationError) as excep:
            validate_license_number(license_number)
        self.assertEqual(
            str(excep.exception),
            "['Last 5 characters should be digits']"
        )

    def test_license_update(self):
        license_number = "ASD12345"
        try:
            validate_license_number(license_number)
        except ValidationError:
            self.fail(
                "Unexpected ValidationError raised for a valid license number"
            )
