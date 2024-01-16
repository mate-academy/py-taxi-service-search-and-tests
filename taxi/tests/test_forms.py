from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForm(TestCase):
    def test_driver_creation_form_with_all_custom_params(self):
        form_data = {
            "username": "test_user",
            "password1": "T1E2S3T4",
            "password2": "T1E2S3T4",
            "last_name": "Test last",
            "first_name": "Test first",
            "license_number": "TES41234",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
