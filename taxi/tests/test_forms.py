from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_valid_data(self):
        form_data = {
            "username": "test_user",
            "license_number": "AAA12345",
            "first_name": "Armen",
            "last_name": "Pagasyan",
            "password1": "pass123QWE",
            "password2": "pass123QWE",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
