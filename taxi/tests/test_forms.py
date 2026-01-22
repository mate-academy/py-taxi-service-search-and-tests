from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestLicenceNumber(TestCase):
    @staticmethod
    def __form_data(license_number: str) -> dict:
        form_data = {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": license_number,
        }
        return form_data

    def test_licence_number_with_length_more_then_eight(self):
        form = DriverCreationForm(
            data=self.__form_data(license_number="A11111111")
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"],
                         ["License number should consist of 8 characters"])

    def test_licence_number_with_length_less_then_eight(self):
        form = DriverCreationForm(data=self.__form_data(license_number="A111"))
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"],
                         ["License number should consist of 8 characters"])

    def test_licence_number_without_uppercase_characters(self):
        form = DriverCreationForm(
            data=self.__form_data(license_number="aaa11111")
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"],
                         ["First 3 characters should be uppercase letters"])

    def test_license_number_with_last_characters_not_digits(self):
        form = DriverCreationForm(
            data=self.__form_data(license_number="AAABBBBB")
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"],
                         ["Last 5 characters should be digits"])

    def test_valid_licence_number(self):
        form = DriverCreationForm(
            data=self.__form_data(license_number="AAA11111")
        )
        self.assertTrue(form.is_valid())
