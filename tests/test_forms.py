from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class LicenseNumberValidationFormTest(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_license_number_is_valid(self):
        self.assertTrue(self.create_form("QWE12345").is_valid())

    def test_length_of_license_number_not_less_than_8(self):
        self.assertFalse(self.create_form("QWE1234").is_valid())

    def test_length_of_license_number_not_more_than_8(self):
        self.assertFalse(self.create_form("QWE123456").is_valid())

    def test_first_3_characters_are_uppercase_letters(self):
        self.assertFalse(self.create_form("QwE123456").is_valid())

    def test_last_5_characters_are_digits(self):
        self.assertFalse(self.create_form("QWER2345").is_valid())
