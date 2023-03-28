from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last(self):
        form_data = {
            "username": "driver_user",
            "password1": "drive12345",
            "password2": "drive12345",
            "first_name": "Driver First",
            "last_name": "Driver Last",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
