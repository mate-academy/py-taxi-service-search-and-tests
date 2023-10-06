from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    validate_license_number,
    DriverLicenseUpdateForm
)


class DriverFormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_username",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "TST00000",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
        }

    def test_driver_creation_form_with_clean_license_number(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_license_update_form_valid(self) -> None:
        form_data = {"license_number": "TST00000"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_validate_invalid_license_number(self) -> None:
        invalid_license_numbers = [
            "TST0000",
            "tst00000",
            "TST0000t",
            "00000000"
        ]
        for license_number in invalid_license_numbers:
            with self.assertRaises(ValidationError):
                validate_license_number(license_number)

    def test_validate_valid_license_number(self) -> None:
        valid_license_numbers = ["TST00000", "XXX12345"]
        for license_number in valid_license_numbers:
            self.assertEqual(
                validate_license_number(license_number),
                license_number
            )
