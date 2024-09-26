from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
    CarForm,
    DriverUpdateInfoForm,
)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_return_correct_field(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "TYU12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_update_return_correct_field(self):
        form_data = {
            "username": "test_username",
            "password": "test_password",
            "license_number": "QWE12345",
        }

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {"license_number": "QWE12345"})

    def test_validate_license_number(self):
        values = {
            "ASD123456": "License number should consist of 8 characters",
            "aSD12345": "First 3 characters should be uppercase letters",
            "BKJ1E345": "Last 5 characters should be digits"
        }
        for license_number, error in values.items():
            with self.assertRaises(ValidationError) as context:
                validate_license_number(license_number)

            self.assertTrue(error in context.exception)


class DriverUpdateInfoFormTest(TestCase):
    def test_driver_form_return_correct_fields(self):
        form_data = {
            "username": "test_username",
            "password": "test_password",
            "first_name": "name",
            "last_name": "surname",
            "email": "mail@gmail.com",
            "phone_number": "number",
        }

        form = DriverUpdateInfoForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data,
            {
                "email": "mail@gmail.com",
                "first_name": "name",
                "last_name": "surname",
                "phone_number": "number",
            },
        )
