from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_license_number_first_last_name(self):
        form_data = {
            "username": "testname",
            "password1": "Test12345",
            "password2": "Test12345",
            "license_number": "BCA32541",
            "first_name": "name",
            "last_name": "surname"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
