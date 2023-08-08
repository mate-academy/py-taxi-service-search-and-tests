from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_with_license_first_last_is_valid(self):
        form_data = {
            "username": "driver",
            "password1": "pass123456",
            "password2": "pass123456",
            "first_name": "driver",
            "last_name": "driver",
            "license_number": "MIT45625",
        }

        form = DriverCreationForm(form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, form_data)
