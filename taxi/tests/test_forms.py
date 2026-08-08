from django import forms
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)


class DriverCreationFormTests(TestCase):
    def test_driver_creation_form_with_valid_license_is_valid(self):
        form_data = {
            "username": "john",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_driver_creation_form_with_invalid_license_length(self):
        form_data = {
            "username": "john",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "ABC1234",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_with_invalid_license_prefix(self):
        form_data = {
            "username": "john",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "abc12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_with_invalid_license_suffix(self):
        form_data = {
            "username": "john",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "ABC12AAA",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_update_form_with_valid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "XYZ54321"}
        )

        self.assertTrue(form.is_valid())

    def test_update_form_with_invalid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "12345678"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTests(TestCase):
    def test_drivers_field_uses_checkbox_select_multiple(self):
        form = CarForm()

        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple,
        )
