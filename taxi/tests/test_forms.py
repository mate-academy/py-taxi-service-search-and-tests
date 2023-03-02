from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "admin1223",
            "password1": "admintestspass",
            "password2": "admintestspass",
            "first_name": "Volkswagen",
            "last_name": "Germany",
            "license_number": "VOL12345"
        }
        self.driver = DriverCreationForm(data=self.form_data)

    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_driver_creation_form_with_license_number_name_is_valid(self):
        self.assertTrue(self.driver.is_valid())
        self.assertEqual(self.driver.cleaned_data, self.form_data)

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("ABC12325").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("TES123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("QWE1334").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("DF122456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("REDF2245").is_valid())
