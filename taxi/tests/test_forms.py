from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form_with_model_license_first_last_name(self):
        form_data = {
            "username": "new_user",
            "password1": "PASSWORD911",
            "password2": "PASSWORD911",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Smith",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
