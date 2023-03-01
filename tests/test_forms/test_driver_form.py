from django.test import TestCase

from taxi.forms import DriverForm


class DriverFormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "testuser",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ESS12345"
        }
        self.form = DriverForm(self.form_data)

    def test_driver_form_with_license_number_first_last_name_is_valid(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)

    def test_driver_form_license_number_first_3_symbol_is_alphabet(self):
        self.form_data["license_number"] = "QW123456"
        self.assertFalse(DriverForm(self.form_data).is_valid())

    def test_driver_form_license_number_first_3_symbol_is_upper(self):
        self.form_data["license_number"] = "QwE12345"
        self.assertFalse(DriverForm(self.form_data).is_valid())

    def test_driver_form_license_number_last_5_symbol_is_digit(self):
        self.form_data["license_number"] = "QWER1234"
        self.assertFalse(DriverForm(self.form_data).is_valid())

    def test_driver_form_license_number_length_less_8_digits(self):
        self.form_data["license_number"] = "QWE12"
        self.assertFalse(DriverForm(self.form_data).is_valid())

    def test_driver_form_license_number_length_bigger_8_digits(self):
        self.form_data["license_number"] = "QWER123456"
        self.assertFalse(DriverForm(self.form_data).is_valid())
