from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_first_last_name_license_num(self):
        form_data = {
            "username": "max_black",
            "first_name": "max",
            "last_name": "black",
            "password1": "pasword2234",
            "password2": "pasword2234",
            "license_number": "AVD12335",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
