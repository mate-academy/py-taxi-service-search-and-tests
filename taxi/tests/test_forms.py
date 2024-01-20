from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_custom_fields(self):
        form_fields_data = {
            "username": "TestUsername",
            "password1": "Test123321#",
            "password2": "Test123321#",
            "license_number": "XML00000",
            "first_name": "Test First",
            "last_name": "Test Last"
        }
        form = DriverCreationForm(data=form_fields_data)

        if not form.is_valid():
            print(f"Error in validation: {form.errors}")

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_fields_data)
