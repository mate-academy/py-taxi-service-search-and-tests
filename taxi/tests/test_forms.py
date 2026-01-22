from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "AAA11111",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        cleaned_data = form.cleaned_data
        cleaned_data.pop("password1")
        cleaned_data.pop("password2")
        self.assertEqual(cleaned_data, {
            "username": "testuser",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "AAA11111",
        })
