from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_driver_creation_form(self):
        """
        Test that driver creation form
        have fields first_name, last_name and
        license number
        """
        form_data = {
            "username": "test_user",
            "password1": "test_pass",
            "password2": "test_pass",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "AAA33333"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
