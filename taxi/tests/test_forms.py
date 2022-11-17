from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_license_number(self):
        form_data = {
            "username": "testusername",
            "password1": "TESTpassword123",
            "password2": "TESTpassword123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
