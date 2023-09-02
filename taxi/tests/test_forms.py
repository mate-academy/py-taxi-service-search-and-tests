from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTests(TestCase):
    def test_field_labels(self):
        form = DriverCreationForm()

        self.assertTrue(
            form.fields["license_number"].label is None
            or form.fields["license_number"].label == "License number"
        )
        self.assertTrue(
            form.fields["first_name"].label is None
            or form.fields["first_name"].label == "First name"
        )
        self.assertTrue(
            form.fields["last_name"].label is None
            or form.fields["last_name"].label == "Last name"
        )

    def test_license_number_too_long(self):
        form_data = {
            "username": "testerr",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "ABC123456"
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_license_number_starts_with_two_letters(self):
        form_data = {
            "username": "testerr",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "AB012345"
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_license_number_starts_with_lowercase_letters(self):
        form_data = {
            "username": "testerr",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "abc12345"
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_license_number_ends_with_four_digits(self):
        form_data = {
            "username": "testerr",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "ABCD1234"
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_livense_number_valid(self):
        form_data = {
            "username": "testerr",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data, form_data)


class DriverUpdateFormTests(TestCase):
    def test_field_labels(self):
        form = DriverCreationForm()

        self.assertTrue(
            form.fields["license_number"].label is None
            or form.fields["license_number"].label == "License number"
        )

    def test_update_driver_license(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data, form_data)

    def test_driver_license_validation(self):
        form_data_list = [
            {"license_number": "ABC123456"},
            {"license_number": "ABCD1234"},
            {"license_number": "AB012345"},
            {"license_number": "abc12345"},
        ]

        for form_data in form_data_list:
            form = DriverLicenseUpdateForm(data=form_data)

            self.assertFalse(form.is_valid())
