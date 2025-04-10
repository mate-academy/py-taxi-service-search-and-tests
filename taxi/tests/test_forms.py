from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormTests(TestCase):
    def test_driver_form(self):
        form_data = {
            "username": "user",
            "email": "mail@i.ii",
            "password1": "Strsword123",
            "password2": "Strsword123",
            "first_name": "first",
            "last_name": "last",
            "license_number": "TTT55555",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), )
        self.assertEqual(form.cleaned_data["username"],
                         form_data["username"]
                         )
        self.assertEqual(form.cleaned_data["first_name"],
                         form_data["first_name"]
                         )
        self.assertEqual(form.cleaned_data["last_name"],
                         form_data["last_name"]
                         )
        self.assertEqual(form.cleaned_data["license_number"],
                         form_data["license_number"]
                         )
