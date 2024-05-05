from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number
)


class FormTests(TestCase):
    def test_driver_creation_form_with_first_last_name_license_number_is_valid(
            self
    ):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_number_update_form_is_valid(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_validate_license_number_with_valid_input(self):
        license_number = "ABC12345"
        validated_license_number = validate_license_number(license_number)
        self.assertEqual(validated_license_number, license_number)

    def test_validate_license_number_with_invalid_input(self):
        invalid_license_number = "invalid license"

        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)
