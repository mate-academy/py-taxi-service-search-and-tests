from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TST12345"
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_driver_creation_form_with_extra_fields_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_license_number_is_valid(self):
        self.form.save()

        self.assertEqual(
            self.form.cleaned_data["license_number"],
            self.form_data["license_number"],
            "License number should be in next format: 'ABC12345'"
        )
        self.assertEqual(self.form.cleaned_data, self.form_data)

    def test_if_can_authenticate(self):
        driver = self.form.save()

        self.assertIsInstance(driver, get_user_model())
        self.assertTrue(
            authenticate(
                username=self.form_data["username"],
                password=self.form_data["password1"]
            )
        )


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_number_is_valid_after_update(self):
        form_data = {
            "license_number": "TST54321"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number_length(self):
        license_numbers = [
            "TS1234567", "TST1234", "TST 12345"
        ]
        for license_number in license_numbers:
            form_data = {
                "license_number": license_number
            }
            form = DriverLicenseUpdateForm(data=form_data)
            self.assertFalse(form.is_valid())

    def test_invalid_license_number_format(self):
        license_numbers = [
            "TS123456", "tst12345", "12345678", "TEST1234", "1T2S3T45", "12345TST"
        ]
        for license_number in license_numbers:
            form_data = {
                "license_number": license_number
            }
            form = DriverLicenseUpdateForm(data=form_data)
            self.assertFalse(form.is_valid())
