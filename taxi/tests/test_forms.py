from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_custom_fields_is_valid(self):
        form_data = {
            "username": "testusername",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
