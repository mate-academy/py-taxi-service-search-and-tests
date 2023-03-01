from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class DriverLicenseUpdateFormTests(TestCase):
    @staticmethod
    def create_form(test_number):
        return DriverLicenseUpdateForm({"license_number": test_number})

    def test_license_number_with_valid_data_is_valid(self):
        self.assertTrue(self.create_form("QWE12345").is_valid())

    def test_license_number_first_3_symbol_is_alphabet(self):
        self.assertFalse(self.create_form("QW123456").is_valid())

    def test_license_number_first_3_symbol_is_upper(self):
        self.assertFalse(self.create_form("QwE12345").is_valid())

    def test_license_number_last_5_symbol_is_digit(self):
        self.assertFalse(self.create_form("QWER1234").is_valid())

    def test_license_number_length_less_8_digits(self):
        self.assertFalse(self.create_form("QWE12").is_valid())

    def test_license_number_length_bigger_8_digits(self):
        self.assertFalse(self.create_form("QWER123456").is_valid())
