from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "hoakin",
            "password1": "a0s9d8f7",
            "password2": "a0s9d8f7",
            "first_name": "Hoa",
            "last_name": "Kin",
            "license_number": "PLO19283"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
