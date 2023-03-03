from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class TestDriverCreationForm(TestCase):

    def setUp(self) -> None:
        self.form_driver = {
            "username": "nick",
            "password1": "abcdefg12345",
            "password2": "abcdefg12345",
            "email": "aaa@ff.com",
            "first_name": "Jo",
            "last_name": "Bush",
            "license_number": "AAA12345"
        }
        self.form = DriverCreationForm(self.form_driver)

    def test_driver_form_has_license_number_first_name_last_name(self):
        self.assertTrue(self.form.is_valid())

    def test_that_license_number_start_with_3_upper_letter(self):
        self.form_driver["license_number"] = "AaA12345"
        self.assertFalse(DriverCreationForm(self.form_driver).is_valid())

    def test_driver_form_has_license_number_with_length_8_characters(self):
        self.form_driver["license_number"] = "AAA123456"
        self.assertFalse((DriverCreationForm(self.form_driver).is_valid()))

    def test_that_license_number_has_after_3_letters_5_digits(self):
        self.form_driver["license_number"] = "AAA1234a"
        self.assertFalse(DriverCreationForm(self.form_driver).is_valid())

    def test_that_firs_characters_in_license_number_is_letters(self):
        self.form_driver["license_number"] = "1AA12345"
        self.assertFalse(DriverCreationForm(self.form_driver).is_valid())
