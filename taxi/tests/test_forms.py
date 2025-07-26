from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_first_last_license_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "ABC13112",
            "first_name": "test",
            "last_name": "lastname",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
