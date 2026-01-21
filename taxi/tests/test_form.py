from taxi.forms import DriverCreationForm
from django.test import TestCase


class FormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "DFG12345",
        }

    def test_driver_create_form_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"],
                         self.form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"],
                         self.form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"],
                         self.form_data["last_name"])
        self.assertEqual(form.cleaned_data["license_number"],
                         self.form_data["license_number"])
