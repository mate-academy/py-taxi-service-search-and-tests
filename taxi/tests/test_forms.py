from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_form_with_additional_parameters(self):
        form_data = {
            "username": "OrdinaryUser",
            "password1": "12121212@A",
            "password2": "12121212@A",
            "first_name": "Ordinary",
            "last_name": "User",
            "license_number": "ABC12346"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
