from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form_data = {
            "username": "testless",
            "password1": "letitest17",
            "password2": "letitest17",
            "license_number": "BOR31337",
            "first_name": "Joe",
            "last_name": "Biden"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
