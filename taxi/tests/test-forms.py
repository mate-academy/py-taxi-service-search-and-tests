from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_with_licensenumber_firstname_lastname(self):
        form_data = {
            "username": "test_user",
            "password1": "User123!_k",
            "password2": "User123!_k",
            "first_name": "Test_name",
            "last_name": "Test_surname",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
