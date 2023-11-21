from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "TestUser",
            "password1": "testPass1",
            "password2": "testPass1",
            "first_name": "Test Firstname",
            "last_name": "Test Lastname",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_input_invalid_license_number(self):
        form_data = {
            "username": "TestUser",
            "password1": "testPass1",
            "password2": "testPass1",
            "first_name": "Test Firstname",
            "last_name": "Test Lastname",
            "license_number": "A",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "1"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "QWERTYUI"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "12345678"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "abc12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
