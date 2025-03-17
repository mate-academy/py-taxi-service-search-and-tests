from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "license_number": "PYT12121",
            "first_name": "test_name",
            "last_name": "test_last",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
