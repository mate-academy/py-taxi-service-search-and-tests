from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        cleaned_data = form.cleaned_data
        self.assertEqual(cleaned_data["username"], form_data["username"])
        self.assertEqual(cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(cleaned_data["last_name"], form_data["last_name"])
        self.assertEqual(
            cleaned_data["license_number"],
            form_data["license_number"]
        )
