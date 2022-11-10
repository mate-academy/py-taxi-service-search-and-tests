from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_is_valid_with_first_last_name_license_number(self):
        form_data = {
            "username": "test",
            "password1": "1test1234",
            "password2": "1test1234",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "LIC12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
