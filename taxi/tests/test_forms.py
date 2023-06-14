from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "test123test",
            "password2": "test123test",
            "first_name": "Test first",
            "last_name": "Last test",
            "license_number": "FGD45678"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
