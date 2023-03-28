from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form_with_license_etc_is_valid(self):
        form_data = {
            "username": "test1",
            "password1": "test123456",
            "password2": "test123456",
            "license_number": "TES12345",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
