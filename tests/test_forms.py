from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car
from taxi.views import CarListView


class DriverTest(TestCase):
    def test_driver_creation_form_with_additional_fields(self):
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

    def test_driver_creation_form_with_not_valid_password(self):
        initial_data = {
            "username": "test_username",
            "password1": "test12568",
            "password2": "test128",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "SAF12536",
        }

        form = DriverCreationForm(data=initial_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_not_valid_license(self):
        initial_data = {
            "username": "test_username",
            "password1": "test12568",
            "password2": "test12568",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "SAF136",
        }

        form = DriverCreationForm(data=initial_data)
        self.assertFalse(form.is_valid())
