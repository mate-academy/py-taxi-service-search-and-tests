from django.test import TestCase

from taxi import forms


class FormsTest(TestCase):
    def test_driver_creation_form_has_license_number(self):
        form_data = {
            "username": "username_sad",
            "password1": "<PASSWORD>123",
            "password2": "<PASSWORD>123",
            "license_number": "TES12345",
            "first_name": "<FIRST_NAME>",
            "last_name": "<LAST_NAME>"
        }
        form = forms.DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"], "TES12345")
