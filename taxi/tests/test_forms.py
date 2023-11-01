from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid_license(self):
        form_data = {
            "username": "test_user",
            "password1": "qwert1235y",
            "password2": "qwert1235y",
            "license_number": "QWE12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_no_license(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_letters_numbers(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "QQQQ1111"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "11111111"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "QQQQQQQQ"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_incorrect_length(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "QQQ111111"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "QQQ111"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
