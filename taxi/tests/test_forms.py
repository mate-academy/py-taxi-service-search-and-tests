from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_valid_license(self):
        form_data = {
            "username": "new_user",
            "password1": "user1234",
            "password2": "user1234",
            "first_name": "Test first",
            "last_name": "Test second",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_invalid_license(self):
        form_data = {
            "username": "new_user",
            "password1": "user1234",
            "password2": "user1234",
            "first_name": "Test first",
            "last_name": "Test second",
            "license_number": "test2345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
