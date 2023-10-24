from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid_license(self):
        form_data = {
            "username": "test_user",
            "password1": "carry1235k",
            "password2": "carry1235k",
            "license_number": "JON12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_no_license(self):
        form_data = {
            "username": "test_user",
            "password1": "password1",
            "password2": "password1"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_incorrect_length(self):
        form_data = {
            "username": "test_user",
            "password1": "password1",
            "password2": "password1",
            "license_number": "AAA000000"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        form_data = {
            "username": "test_user",
            "password1": "password1",
            "password2": "password1",
            "license_number": "AAA000"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_letters_numbers(self):
        form_data = {
            "username": "test_user",
            "password1": "password1",
            "password2": "password1",
            "license_number": "AAAA0000"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        form_data = {
            "username": "test_user",
            "password1": "password1",
            "password2": "password1",
            "license_number": "00000000"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        form_data = {
            "username": "test_user",
            "password1": "password1",
            "password2": "password1",
            "license_number": "AAAAAAAA"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
