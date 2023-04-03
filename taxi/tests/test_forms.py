from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverSearchForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "Marichka",
            "password1": "z54bvFG543",
            "password2": "z54bvFG543",
            "first_name": "Maria",
            "last_name": "Clinton",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_license_number_is_invalid(self):
        form_data = {
            "username": "user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "user_name",
            "last_name": "user_last_name",
            "license_number": "INVALID_LICENSE_NUMBER"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_with_missing_license_number(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "test_name",
            "last_name": "test_last_name",
            "license_number": ""
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
