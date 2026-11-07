from django.test import TestCase

from taxi.forms import DriverCreationForm


class MyTestCase(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "new_driver",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "new",
            "last_name": "driver",
            "license_number": "ASD12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
