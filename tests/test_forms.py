from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    validate_license_number
)


class FormsTests(TestCase):
    def test_author_creation_form_with_pseudonym_first_last_name_is_valid(
            self
    ):
        form_data = {
            "username": "new_user",
            "password1": "user1234",
            "password2": "user1234",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_license(self):
        license_number = "ABD12345"
        try:
            validate_license_number(license_number)
        except ValidationError:
            self.fail(
                "Unexpected ValidationError raised for a valid license number"
            )

    def test_invalid_license_number_length(self):
        license_number = "ABC1234"
        with self.assertRaises(ValidationError) as cm:
            validate_license_number(license_number)

        self.assertEqual(
            str(cm.exception),
            "['License number should consist of 8 characters']"
        )

    def test_invalid_license_number_format(self):
        license_number = "abc12345"
        with self.assertRaises(ValidationError) as cm:
            validate_license_number(license_number)

        self.assertEqual(
            str(cm.exception),
            "['First 3 characters should be uppercase letters']"
        )

        license_number = "ABC1X345"
        with self.assertRaises(ValidationError) as cm:
            validate_license_number(license_number)

        self.assertEqual(
            str(cm.exception),
            "['Last 5 characters should be digits']"
        )
