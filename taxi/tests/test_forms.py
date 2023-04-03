from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last(self):
        valid_form_data = {
            "username": "driver_user",
            "password1": "drive12345",
            "password2": "drive12345",
            "first_name": "Driver First",
            "last_name": "Driver Last",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, valid_form_data)

        invalid_license_numbers = [
            {"license_number": "tes12345"},
            {"license_number": "TES123"},
            {"license_number": "123TES"},
            {"license_number": "TES123456"},
            {"license_number": "TES1234A"},
        ]
        for data in invalid_license_numbers:
            form = DriverCreationForm(data={**valid_form_data, **data})
            self.assertFalse(form.is_valid())
