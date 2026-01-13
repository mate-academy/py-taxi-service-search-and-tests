from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_name_last_name(self):
        form_data = {
            "username": "test_user",
            "password1": "test1231",
            "password2": "test1231",
            "first_name": "test_name",
            "last_name": "test_lastname",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], form_data["last_name"])
        self.assertEqual(form.cleaned_data["license_number"], form_data["license_number"])