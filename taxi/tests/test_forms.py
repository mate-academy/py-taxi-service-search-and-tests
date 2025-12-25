from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "QWE12345",

        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
