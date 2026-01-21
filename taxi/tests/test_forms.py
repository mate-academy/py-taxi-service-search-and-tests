from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number
)


class DriverFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "awesome_username",
            "first_name": "awesome_name",
            "last_name": "awesome_last_name",
            "license_number": "ABC12345",
            "password1": "strongestPassword",
            "password2": "strongestPassword",
        }

    def test_form_creation_with_valid_data(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, self.form_data)

    def test_form_update_license_with_valid_license(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_validate_update_license_form(self) -> None:
        invalid_licenses = {
            "12345678",
            "avd12345",
            "123askhj",
            "Avu123456"
        }

        for license_number in invalid_licenses:
            with self.assertRaises(ValidationError):
                validate_license_number(license_number)
