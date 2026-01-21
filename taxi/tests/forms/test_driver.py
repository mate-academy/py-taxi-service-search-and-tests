from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "user_test",
            "password1": "1234pass",
            "password2": "1234pass",
            "first_name": "First test",
            "last_name": "Last test",
            "license_number": "NBA12345"
        }

    def test_form_valid_data(self):
        form = DriverCreationForm(self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def check_invalid_license_number(
            self, invalid_license_number: str,
            message: str
    ):
        self.form_data["license_number"] = invalid_license_number

        form = DriverCreationForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual({"license_number": [message]}, form.errors)

    def test_form_length_smaller_than_eight_in_license_num(self):
        self.check_invalid_license_number(
            invalid_license_number="NBA2345",
            message="License number should consist of 8 characters"
        )

    def test_form_one_letter_is_lower_case_in_license_num(self):
        self.check_invalid_license_number(
            invalid_license_number="NBa12345",
            message="First 3 characters should be uppercase letters"
        )

    def test_form_invalid_last_digits_in_license_num(self):
        self.check_invalid_license_number(
            invalid_license_number="NBA1234a",
            message="Last 5 characters should be digits"
        )


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "license_number": "NBA12345",
        }

    def test_form_valid_data(self):
        form = DriverLicenseUpdateForm(self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def check_invalid_license_number(
            self, invalid_license_number: str,
            message: str
    ):
        self.form_data["license_number"] = invalid_license_number

        form = DriverLicenseUpdateForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual({"license_number": [message]}, form.errors)

    def test_form_length_smaller_than_eight_in_license_num(self):
        self.check_invalid_license_number(
            invalid_license_number="NBA2345",
            message="License number should consist of 8 characters"
        )

    def test_form_one_letter_is_lower_case_in_license_num(self):
        self.check_invalid_license_number(
            invalid_license_number="NBa12345",
            message="First 3 characters should be uppercase letters"
        )

    def test_form_invalid_last_digits_in_license_num(self):
        self.check_invalid_license_number(
            invalid_license_number="NBA1234a",
            message="Last 5 characters should be digits"
        )
