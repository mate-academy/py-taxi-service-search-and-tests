from django.test import TestCase
from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation(self):
        form_data = {
            "username": "admin",
            "password1": "test123456",
            "password2": "test123456",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "UAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "admin")
