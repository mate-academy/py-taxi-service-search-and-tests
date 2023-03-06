from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_driver",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test first name",
            "last_name": "Test last name",
            "license_number": "TST12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
