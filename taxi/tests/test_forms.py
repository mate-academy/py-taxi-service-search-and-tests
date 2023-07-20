from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_username",
            "password1": "test_password123",
            "password2": "test_password123",
            "first_name": "test_first_name",
            "last_name": "test_first_name",
            "license_number": "TES12345"
        }

    def test_creation_form_with_license_number_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_validation_license_number(self):
        form_len = DriverCreationForm(data={"license_number": "TES111111111"})
        self.assertFalse(form_len.is_valid())

        form_first_char = DriverCreationForm(
            data={"license_number": "T9s12345"}
        )
        self.assertFalse(form_first_char.is_valid())

        form_last_digits = DriverCreationForm(
            data={"license_number": "TES12Ya5"}
        )
        self.assertFalse(form_last_digits.is_valid())
