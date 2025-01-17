from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "TES12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        new_driver = form.save()
        self.assertEqual(new_driver.username, form_data["username"])
        self.assertEqual(new_driver.license_number,
                         form_data["license_number"])
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
