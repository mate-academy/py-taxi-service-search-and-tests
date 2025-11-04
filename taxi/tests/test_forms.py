from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi import forms
from taxi.forms import validate_license_number


class FormTest(TestCase):

    def test_driver_create_form(self):
        form_data = {
            "username": "TestDriver",
            "password1": "TestPass1234",
            "password2": "TestPass1234",
            "license_number": "TES33443",
        }
        form = forms.DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_number_validation(self):
        form_data = {
            "username": "TestDriver",
            "password1": "TestPass1234",
            "password2": "TestPass1234",
        }
        test_cases = [
            "TTT4343",
            "TT344351",
            "TTd44352",
            "TTd4435A",
            "TTd4435b",
            "TTHGFSFV",
            "12345678",
        ]

        for license_number in test_cases:
            form_data["license_number"] = license_number
            with self.subTest(form_data=form_data):
                form = forms.DriverLicenseUpdateForm(data=form_data)
                self.assertRaises(
                    ValidationError,
                    validate_license_number,
                    form.instance.license_number,
                )
                self.assertFalse(form.is_valid())
