from django.core.exceptions import ValidationError
from django.test import TestCase
from taxi.forms import DriverCreationForm, validate_license_number


class DriverCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            "first_name": "test First",
            "last_name": "test Last",
            "username": "test_username",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "ABC12345"
        }

    def test_driver_creation_form_with_firs_last_name_license_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_validation_license_number_with_invalid_data(self):
        modified_form_data = self.form_data.copy()
        modified_form_data["license_number"] = "XYZ987654"
        form = DriverCreationForm(data=modified_form_data)

        self.assertFalse(form.is_valid())


class ValidateLicenseNumberTest(TestCase):
    def test_length_more_than_8_characters(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            license_number = "XYZ987654"
            validate_license_number(license_number)

    def test_length_less_than_8_characters(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            license_number = "XYZ9876"
            validate_license_number(license_number)

    def test_first_three_letters_are_lower(self):
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            license_number = "xyz98765"
            validate_license_number(license_number)

    def test_first_three_characters_not_alpha(self):
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            license_number = "12398765"
            validate_license_number(license_number)

    def test_last_five_characters_not_digits(self):
        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
        ):
            license_number = "XYZV8765"
            validate_license_number(license_number)
