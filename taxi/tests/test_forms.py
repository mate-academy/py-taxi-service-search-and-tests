from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password01": "user12test",
            "password02": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_numer": "12345678"
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
