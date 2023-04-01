from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_first_last_name_license_num(self):
        form_data = {
            "username": "adam_eva",
            "first_name": "adam",
            "last_name": "eva",
            "password1": "adam_eva.adam_eva",
            "password2": "adam_eva.adam_eva",
            "license_number": "AVD12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)