from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_driver_form_in_valid(self):
        form_data = {
            "username": "driver1",
            "license_number": "RET12345",
            "first_name": "Driver",
            "last_name": "Driver",
            "password1": "Password!!",
            "password2": "Password!!"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
