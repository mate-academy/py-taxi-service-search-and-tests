from django.test import TestCase
from taxi.forms import DriverCreationForm


class TestForm(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "license_number": "AFH45563",
            "first_name": "Test first",
            "last_name": "Test last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
