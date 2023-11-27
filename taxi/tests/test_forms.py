import unittest
from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_form_with_all_valid_fields(self) -> None:
        form_data = {"username": "test_user",
                     "password1": "test_user_password228",
                     "password2": "test_user_password228",
                     "license_number": "ABD54345",
                     "first_name": "Global",
                     "last_name": "Test"}
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_with_valid_field(self) -> None:
        form_data = {"license_number": "ABD54345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    @staticmethod
    def validate_license_number(license_number):
        form_data = {
            "username": "test_user",
            "password1": "test_user_password228",
            "password2": "test_user_password228",
            "license_number": license_number,
            "first_name": "Global",
            "last_name": "Test"
        }
        form = DriverCreationForm(data=form_data)
        return form.is_valid()

    @unittest.expectedFailure
    def test_license_number_format(self):
        test_cases = [
            ("XYZ98765", True),
            ("LMN12345", True),
            ("PQR67890", True),
            ("ZYX1234A", False),
            ("1ABCD234", False),
            ("INVALID", False),
            ("11111XYZ", False),
            ("X9876543", False),
            ("AA11BB22", False),
            ("987", False),
            ("AAA111", False),
            ("XYZZYX", False),
            ("X", False)
        ]

        for license_number, expected_result in test_cases:
            with self.subTest(license_number=license_number):
                self.assertEqual(
                    self.validate_license_number(license_number),
                    expected_result
                )
