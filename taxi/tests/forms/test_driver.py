from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "bob",
            "password1": "1234s#$SSf",
            "password2": "1234s#$SSf",
            "first_name": "bob",
            "last_name": "max",
            "license_number": "CCC12345"
        }

    def test_form_valid_data(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def driver_create_invalid_license_number(
            self, invalid_license_number: str,
            message: str
    ):
        self.form_data["license_number"] = invalid_license_number
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual({"license_number": [message]}, form.errors)

    def test_license_number_short_length(self):
        self.driver_create_invalid_license_number(
            invalid_license_number="qwe123w",
            message="License number should consist of 8 characters"
        )

    def test_invalid_first_three_chars(self):
        self.driver_create_invalid_license_number(
            invalid_license_number="qwe51234",
            message="First 3 characters should be uppercase letters"
        )

    def test_invalid_digits(self):
        self.driver_create_invalid_license_number(
            invalid_license_number="QWE!1234",
            message="Last 5 characters should be digits"
        )


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "license_number": "CCC12345",
        }

    def test_form_valid_data(self):
        form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def driver_update_invalid_license_number(
            self, invalid_license_number: str,
            message: str
    ):
        self.form_data["license_number"] = invalid_license_number
        form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual({"license_number": [message]}, form.errors)

    def test_license_number_short_length(self):
        self.driver_update_invalid_license_number(
            invalid_license_number="L23",
            message="License number should consist of 8 characters"
        )

    def test_invalid_first_three_chars(self):
        self.driver_update_invalid_license_number(
            invalid_license_number="ccc51234",
            message="First 3 characters should be uppercase letters"
        )

    def test_invalid_digits(self):
        self.driver_update_invalid_license_number(
            invalid_license_number="BWE&?234",
            message="Last 5 characters should be digits"
        )
