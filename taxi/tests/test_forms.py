from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form_with_license_is_valid(self):
        form_data = {
            "username": "test_driver",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
