from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormsTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "testusername",
            "password1": "1asdfga3",
            "password2": "1asdfga3",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data, form_data)
