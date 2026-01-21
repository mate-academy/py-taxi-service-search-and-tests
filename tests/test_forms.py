from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_and_names_is_valid(self):
        form_data = {
            "username": "User_user",
            "password1": "passwordtest",
            "password2": "passwordtest",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "USE12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_number_length(self):
        message = "License number should consist of 8 characters"
        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number("USE1234")

    def test_validate_license_number_3_first_characters_uppercase(self):
        message = "First 3 characters should be uppercase letters"
        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number("uSE12345")

    def test_validate_license_number_5_last_characters_digits(self):
        message = "Last 5 characters should be digits"
        with self.assertRaisesMessage(ValidationError, message):
            validate_license_number("USE1234u")
