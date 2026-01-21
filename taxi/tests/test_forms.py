from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "name_user",
            "password1": "fgfg123123",
            "password2": "fgfg123123",
            "first_name": "Pipi",
            "last_name": "Kell",
            "license_number": "AAA12312"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
