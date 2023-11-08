from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import (
    DriverCreationForm, DriverLicenseUpdateForm
)


class FormTests(TestCase):
    def test_driver_creation_form_with_all_fields_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "username",
            "password1": "123password321",
            "password2": "123password321",
            "license_number": "ABC12345",
            "first_name": "first_name",
            "last_name": "last_name",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_with_field_is_valid(self) -> None:
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_format(self) -> None:
        valid_license_numbers = [
            "ABC12345", "XYZ67890",
        ]
        invalid_license_numbers = [
            "AB12345",
            "ABCD123456",
            "abc12345",
            "ABc12345",
            "ABC12abc",
            "ABC1234A",
        ]

        for license_number in valid_license_numbers:
            form_data = {
                "username": "username",
                "password1": "123password321",
                "password2": "123password321",
                "license_number": license_number,
                "first_name": "first_name",
                "last_name": "last_name",
            }
            form = DriverCreationForm(data=form_data)
            self.assertTrue(form.is_valid())

        for license_number in invalid_license_numbers:
            form_data = {
                "username": "username",
                "password1": "123password321",
                "password2": "123password321",
                "license_number": license_number,
                "first_name": "first_name",
                "last_name": "last_name",
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
