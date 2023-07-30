from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    form_data = {
        "username": "driver",
        "password1": "pwd12345pwd",
        "password2": "pwd12345pwd",
        "first_name": "Tester",
        "last_name": "Testenko"
    }

    def test_driver_creation_form_with_license_firs_last_name_is_valid(self):
        self.form_data["license_number"] = "TST56789"
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_with_more_than_8_characters_license_number(self):
        self.form_data["license_number"] = "TST567895"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters"
        )

    def test_driver_creation_form_with_only_numbers_license_number(self):
        self.form_data["license_number"] = "12356789"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters"
        )

    def test_driver_creation_form_with_lowercase_series_license_number(self):
        self.form_data["license_number"] = "tst56789"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters"
        )

    def test_driver_creation_form_with_letters_in_number_license_number(self):
        self.form_data["license_number"] = "TST56TS9"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            ValidationError,
            "Last 5 characters should be digits"
        )
