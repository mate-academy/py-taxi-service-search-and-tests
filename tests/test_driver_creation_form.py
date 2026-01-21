from django.test import TestCase
from taxi.forms import DriverCreationForm


class DriverCreationFormTests(TestCase):
    def test_driver_creation_form_clean_license_number(self):
        form_data = {
            "username": "driver3",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "license_number": "ABC12345",
            "first_name": "Michael",
            "last_name": "Johnson",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
