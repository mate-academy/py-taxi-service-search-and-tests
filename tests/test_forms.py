from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
    validate_license_number,
    DriverLicenseUpdateForm,
    DriverCreationForm
)


class FormsTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_number_func(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number("ABC12")

        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("ABc12345")

        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("AB012345")

        with self.assertRaisesMessage(
                ValidationError, "Last 5 characters should be digits"
        ):
            validate_license_number("ABCD2345")

        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_manufacturer_search_form(self):
        form_data = {"name": "Test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form(self):
        form_data = {"model": "Test"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form(self):
        form_data = {"username": "Test"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
