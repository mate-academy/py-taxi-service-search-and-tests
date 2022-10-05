from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class TstDriverCreationForm(TestCase):
    def test_driver_creation_form(self):
        data = {
            "username": "admin321",
            "password1": "grtyh12345",
            "password2": "grtyh12345",
            "first_name": "Andrew",
            "last_name": "Brown",
            "license_number": "QWE98726"
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_validate_license_number(self):
        license_number = "DFE98173"
        self.assertTrue(validate_license_number(license_number))
