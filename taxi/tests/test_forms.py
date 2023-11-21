from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, validate_license_number


class FormTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(
            self
    ):
        form_data = {
            "username": "test_user",
            "password1": "1357Test_password",
            "password2": "1357Test_password",
            "license_number": "ASD45678",
            "first_name": "First",
            "last_name": "Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_number_with_invalid_data(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number("000")

        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("asd45678")

        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
        ):
            validate_license_number("ASD4567a")
