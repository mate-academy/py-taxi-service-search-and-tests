from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class TstDriverCreationForm(TestCase):
    def test_driver_creation_form(self):
        data = {
            "username": "test_user",
            "password1": "12345poiu",
            "password2": "12345poiu",
            "first_name": "Name",
            "last_name": "Lastname",
            "license_number": "AAA11111"
        }

        form = DriverCreationForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_validate_license_number(self):
        license_number = "ASD12345"

        self.assertTrue(validate_license_number(license_number))
