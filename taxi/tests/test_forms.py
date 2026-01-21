from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTestCase(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        test_data = {
            "username": "test_user",
            "license_number": "NNN12345",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "<PASSWORD>",
        }

        form = DriverCreationForm(data=test_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.cleaned_data, test_data)
