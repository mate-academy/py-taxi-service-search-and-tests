from django.test import TestCase
from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_driver_form(self):
        form_data = {
            "username": "driveritto",
            "license_number": "BCA12345",
            "first_name": "Joe",
            "last_name": "Dou",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
