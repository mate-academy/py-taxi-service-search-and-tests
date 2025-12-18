from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import (
    validate_license_number,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Driver


class LicenseNumberValidationTest(TestCase):

    def test_valid_license_number(self):
        license_number = "ABC12345"
        result = validate_license_number(license_number)
        self.assertEqual(result, license_number)

    def test_invalid_length(self):
        with self.assertRaisesMessage(
            ValidationError, "License number should consist of 8 characters"
        ):
            validate_license_number("ABC123")

    def test_invalid_first_letters(self):
        with self.assertRaisesMessage(
            ValidationError, "First 3 characters should be uppercase letters"
        ):
            validate_license_number("abC12345")

    def test_invalid_last_digits(self):
        with self.assertRaisesMessage(
            ValidationError, "Last 5 characters should be digits"
        ):
            validate_license_number("ABC12A45")


class DriverCreationFormTest(TestCase):

    def test_form_is_valid_with_correct_license(self):
        form_data = {
            "username": "driver1",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_wrong_license(self):
        form_data = {
            "username": "driver2",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "abc123",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):

    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver",
            password="pass12345",
            license_number="ABC12345"
        )

    def test_update_with_valid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "XYZ54321"},
            instance=self.driver
        )
        self.assertTrue(form.is_valid())

    def test_update_with_invalid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "wrong"},
            instance=self.driver
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarModelSearchFormTest(TestCase):

    def test_search_form_accepts_value(self):
        form = CarModelSearchForm(data={"model": "BMW"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "BMW")


class DriverUsernameSearchFormTest(TestCase):

    def test_username_search_form(self):
        form = DriverUsernameSearchForm(data={"username": "john"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "john")


class ManufacturerNameSearchFormTest(TestCase):

    def test_manufacturer_search_form(self):
        form = ManufacturerNameSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")
