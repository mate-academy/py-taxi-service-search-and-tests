from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)


Driver = get_user_model()


class DriverCreationFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_driver_data = {
            "username": "valid1",
            "password1": "Paswtewtweyerudfgord123456",
            "password2": "Paswtewtweyerudfgord123456",
            "license_number": "ZYI12345",
        }
        cls.invalid_driver_data = {
            "username": "invalid1",
            "password1": "Paswtewtweyerudfgord123456",
            "password2": "Paswtewtweyerudfgord123456",
            "license_number": "A2C12a45",
        }

    def test_form_fields(self):
        form = DriverCreationForm()
        self.assertIn("username", form.fields)
        self.assertIn("password1", form.fields)
        self.assertIn("password2", form.fields)
        self.assertIn("license_number", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)

    def test_valid_license_number(self):
        form = DriverCreationForm(data=self.valid_driver_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self):
        form = DriverCreationForm(data=self.invalid_driver_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_license_number = "ASW93452"
        cls.too_short_license_number = "ASW9345"
        cls.too_long_license_number = "ASW934521"
        cls.too_many_letters = "ASWA3452"
        cls.too_many_numbers = "AS193452"

    def test_form_fields(self):
        form = DriverLicenseUpdateForm()
        self.assertIn("license_number", form.fields)

    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": self.valid_license_number}
        )
        self.assertTrue(form.is_valid())

    def test_too_short_licence_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": self.too_short_license_number}
        )
        self.assertFalse(form.is_valid())

    def test_too_long_license_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": self.too_long_license_number}
        )
        self.assertFalse(form.is_valid())

    def test_too_many_letters(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": self.too_many_letters}
        )
        self.assertFalse(form.is_valid())

    def test_too_many_numbers(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": self.too_many_numbers}
        )
        self.assertFalse(form.is_valid())


class CarSearchFormTests(TestCase):
    def test_form_fields(self):
        form = CarSearchForm()
        self.assertIn("model", form.fields)

        self.assertIsInstance(form.fields["model"].widget, forms.TextInput)

        self.assertEqual(form.fields["model"].label, "")

        self.assertEqual(
            form.fields["model"].widget.attrs["class"],
            "form-control"
        )
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model..."
        )


class DriverSearchFormTests(TestCase):
    def test_form_fields(self):
        form = DriverSearchForm()
        self.assertIn("username", form.fields)

        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)

        self.assertEqual(form.fields["username"].label, "")

        self.assertEqual(
            form.fields["username"].widget.attrs["class"],
            "form-control"
        )
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username..."
        )


class ManufacturerSearchFormTests(TestCase):
    def test_form_fields(self):
        form = ManufacturerSearchForm()
        self.assertIn("name", form.fields)

        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)

        self.assertEqual(form.fields["name"].label, "")

        self.assertEqual(
            form.fields["name"].widget.attrs["class"],
            "form-control"
        )
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name..."
        )
