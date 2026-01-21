from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "Test_user",
            "password1": "testPass1",
            "password2": "testPass1",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_input_invalid_license_number(self):
        form_data = {
            "username": "Test_user",
            "password1": "testPass1",
            "password2": "testPass1",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "A",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "1"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "ABC"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "13423"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "ABCASDFG"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "12345678"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "abc12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "ABc12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
