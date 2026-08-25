from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm
)


class DriverFormTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.base_data = {
                "username": "test_username",
                "password1": "test_password",
                "password2": "test_password",
            }

    def test_valid_driver_creation_form(self):
        form = DriverCreationForm(
            data={
                **self.base_data,
                "license_number": "ABC12345"
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_driver_creation_form(self):
        invalid_license_numbers = [
            "1234",
            "ABCD1234",
            "AB123456"
        ]

        for license_number in invalid_license_numbers:
            form = DriverCreationForm(
                data={
                    **self.base_data,
                    "license_number": license_number
                }
            )
            self.assertFalse(form.is_valid())

    def test_valid_driver_license_update_form(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_driver_license_update_form(self):
        invalid_license_numbers = [
            "1234",
            "ABCD1234",
            "AB123456"
        ]

        for license_number in invalid_license_numbers:
            form = DriverLicenseUpdateForm(
                data={"license_number": license_number}
            )
            self.assertFalse(form.is_valid())


