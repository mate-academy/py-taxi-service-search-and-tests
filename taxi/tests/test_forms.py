from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_creation_form_with_first_last_name_license_number_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "usertest1234",
            "password2": "usertest1234",
            "first_name": "test name",
            "last_name": "test surname",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_len_drivers_license_number_less_than_8_is_not_valid(self):
        form_data = {
            "username": "test",
            "password1": "usertest1234",
            "password2": "usertest1234",
            "first_name": "test name",
            "last_name": "test surname",
            "license_number": "TES1235"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_first_3_character_of_license_number_not_upper_is_not_valid(self):
        form_data = {
            "username": "test",
            "password1": "usertest1234",
            "password2": "usertest1234",
            "first_name": "test name",
            "last_name": "test surname",
            "license_number": "tes12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_last_3_character_of_license_number_not_numbers_is_not_valid(self):
        form_data = {
            "username": "test",
            "password1": "usertest1234",
            "password2": "usertest1234",
            "first_name": "test name",
            "last_name": "test surname",
            "license_number": "testtest"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
