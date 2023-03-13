from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTest(TestCase):
    def test_create_driver_license_number_first_and_last_name_is_valid(self):
        form_data = {
            "username": "admin",
            "first_name": "name",
            "last_name": "last",
            "license_number": "ASW12345",
            "password1": "admin12345",
            "password2": "admin12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_create_driver_with_incorrect_license_number_is_not_valid(self):
        form_data = {
            "username": "admin",
            "first_name": "name",
            "last_name": "last",
            "license_number": "not_valid",
            "password1": "admin12345",
            "password2": "admin12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_update_license_number_with_incorrect_data(self):
        form_data = {
            "license_number": "not_valid",
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
