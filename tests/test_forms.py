from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverTest(TestCase):
    def driver_creation_form_with_additional_fields(self):
        initial_data = {
            "username": "test_username",
            "password1": "test12568",
            "password2": "test12568",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "SAF12536",
        }

        form = DriverCreationForm(data=initial_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, initial_data)
