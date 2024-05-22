from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form_with_valid_license_and_another_info(self):
        form_data = {
            "username": "user_test",
            "password1": "testPASSWORD12",
            "password2": "testPASSWORD12",
            "license_number": "KAE12312",
            "first_name": "Anthony",
            "last_name": "Joshua"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
