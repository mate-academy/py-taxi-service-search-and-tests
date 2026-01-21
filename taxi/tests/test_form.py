from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_form_with_license_first_last_name(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password1",
            "password2": "test_password1",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "AMG54335",
        }
        form = DriverCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
