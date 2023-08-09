from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    validate_license_number
)


class FormTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "TestUsername",
            "password1": "TestPassword",
            "password2": "TestPassword",
            "license_number": "ABC12345",
            "first_name": "TestFirstName",
            "last_name": "TestLastName"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_username_search_form(self):
        form = DriverUsernameSearchForm()

        self.assertTrue(form.fields["username"].label == "")
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )

    def test_driver_validate_license_number_raise_correct_error_message(self):
        license_numbers_with_message = {
            "short_license_number": (
                "AB12345", "License number should consist of 8 characters"
            ),
            "license_number_without_letter": (
                "AB123456", "First 3 characters should be uppercase letters"
            ),
            "license_number_without_digit": (
                "ABCD1234",
                "Last 5 characters should be digits"
            )
        }
        for information in license_numbers_with_message.values():
            license_number, message = information
            with self.assertRaisesMessage(ValidationError, message):
                validate_license_number(license_number)

    def test_car_search_form(self):
        form = CarModelSearchForm()

        self.assertTrue(form.fields["model"].label == "")
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model"
        )

    def test_manufacturer_name_search_form(self):
        form = ManufacturerNameSearchForm()

        self.assertTrue(form.fields["name"].label == "")
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )
