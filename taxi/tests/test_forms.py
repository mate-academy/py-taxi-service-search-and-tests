from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_names_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "qweert123456!!",
            "password2": "qweert123456!!",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
