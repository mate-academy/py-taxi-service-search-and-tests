from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        """
        Checking valid form
        """
        form_data = {
            "license_number": "AAA12345",
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_update_valid_license_number_less_8(self):
        form_data = {
            "license_number": "AAA1234",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_more_8(self):
        form_data = {
            "license_number": "AAA123456",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_first_3_characters_upper_case(self):
        form_data = {
            "license_number": "aAA1234",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_first_3_charas_upper_letters(self):
        form_data = {
            "license_number": "12345678",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_last_5_characters_are_digits(self):
        form_data = {
            "license_number": "AAA1234a",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())
