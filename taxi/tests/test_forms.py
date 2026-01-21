from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_driver_form_with_custom_fields(self):
        form_data = {
            "username": "new_user",
            "password1": "<PASSWORD12>",
            "password2": "<PASSWORD12>",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
            "license_number": "ARM56984",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
