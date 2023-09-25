from django.test import TestCase
from taxi.forms import DriverLicenseUpdateForm


class ValidLicenseNumberFormTests(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("TES12345").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("TES123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("TES1234").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("TE123456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("TEST2345").is_valid())
