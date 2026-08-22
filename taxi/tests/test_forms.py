from django import forms
from django.test import TestCase

from taxi.forms import DriverCreationForm, CarForm, DriverLicenseUpdateForm


class TestDriverCreationForm(TestCase):
    def test_driver_creation_form_with_valid_data(self):
        form = DriverCreationForm(
            data={
                "username": "Tom",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "license_number": "ABC12345",
                "first_name": "Tom",
                "last_name": "Smith",
            }
        )

        self.assertTrue(form.is_valid())

    def test_license_number_with_lowercase_letters_is_invalid(self):
        form = DriverCreationForm(
            data={
                "username": "Tom",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "license_number": "abc12345",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_invalid_length_of_letters(self):
        form = DriverCreationForm(
            data={
                "username": "Tom",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "license_number": "ABC12345341123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class TestCarForm(TestCase):
    def test_fields_in_car_form(self):
        form = CarForm()

        self.assertIsInstance(
            form.fields["drivers"],
            forms.ModelMultipleChoiceField
        )

        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )


class TestDriverLicenseUpdateForm(TestCase):
    def test_driver_license_update_form_with_correct_data(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})

        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345ABCSA"})

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
