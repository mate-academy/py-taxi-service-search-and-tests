from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_valid_data(self):
        form_data = {
            "username": "anton_best",
            "password1": "anton12345",
            "password2": "anton12345",
            "first_name": "Anton",
            "last_name": "Best",
            "license_number": "AA0031AO",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
