from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_create_driver_form_with_license_number_first_name_last_name(self):
        form_data = {
            "username": "test_name",
            "license_number": "NNN12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",

        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_create_driver_form_invalid_len_numbers_license_number(self):
        form_data = {
            "username": "test_name",
            "license_number": "NNN1234",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",

        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEquals(form.cleaned_data, form_data)

    def test_create_driver_form_invalid_letter_license_number(self):
        form_data = {
            "username": "test_name",
            "license_number": "aQN12342",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",

        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEquals(form.cleaned_data, form_data)

    def test_create_driver_form_invalid_len_letters_license_number(self):
        form_data = {
            "username": "test_name",
            "license_number": "QW12342",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",

        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEquals(form.cleaned_data, form_data)
