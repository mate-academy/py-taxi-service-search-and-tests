from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    validate_license_number,
    DriverLicenseUpdateForm,
    DriverCreationForm
)


class ValidateLicenseNumberTest(TestCase):
    def test_validate_license_number_with_valid_data(self):
        valid_numbers = ["ABC12345", "XYZ98765"]

        for number in valid_numbers:
            result = validate_license_number(number)
            self.assertEqual(result, number)

    def test_validate_license_number_with_invalid_data(self):
        # Invalid license numbers
        invalid_numbers = {
            "ABCD1234": "Last 5 characters should be digits",
            "12345678": "First 3 characters should be uppercase letters",
            "123456ABCDEFG": "License number should consist of 8 characters",
            "1": "License number should consist of 8 characters",
        }
        for number in invalid_numbers:
            with self.assertRaises(ValidationError) as context:
                validate_license_number(number)

            self.assertIn(invalid_numbers[number], str(context.exception))


class DriverCreationLicenseUpdateFormsTest(TestCase):
    def setUp(self):
        self.data = {"license_number": "ABC12345"}
        self.testing_forms = (DriverLicenseUpdateForm, DriverCreationForm)

    def test_driver_create_license_update_form_with_missing_data(self):
        for testing_form in self.testing_forms:
            form = testing_form()
            self.assertIsInstance(form, testing_form)
            self.assertFalse(form.is_valid())

    def test_driver_license_update_with_valid_data(self):
        form = DriverLicenseUpdateForm(self.data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_with_invalid_license_number(self):
        form = DriverLicenseUpdateForm({"license_number": "invalid"})
        self.assertFalse(form.is_valid())

    def test_driver_create_with_valid_and_invalid_data(self):
        license_numbers = ("ABC12345", "invalid")
        for license_number in license_numbers:
            data = {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
                "license_number": license_number,
                "first_name": "Billy",
                "last_name": "Bonce",
            }
            form = DriverCreationForm(data)
            if license_numbers[0] == license_number:
                self.assertTrue(form.is_valid())
            else:
                self.assertFalse(form.is_valid())

    def test_custom_validation_called(self):
        with patch(
                "taxi.forms.validate_license_number"
        ) as mock_validate_license_number:
            for testing_form in self.testing_forms:
                form = testing_form(self.data)
                form.is_valid()
                mock_validate_license_number.assert_called_with(
                    self.data["license_number"]
                )
