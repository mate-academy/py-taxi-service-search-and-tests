from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_update_valid_license_number_length_less_8(self):
        form_data = {
            "license_number": "TES1234",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_length_more_8(self):
        form_data = {
            "license_number": "TES123456",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_first_3_characters_upper(self):
        form_data = {
            "license_number": "Tes12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_licen_number_first_must_contain_3_char_upp(self):
        form_data = {
            "license_number": "12345678",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_last_5_characters_are_digits(self):
        form_data = {
            "license_number": "TES1234S",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())
