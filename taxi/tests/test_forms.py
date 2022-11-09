from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        data = {
            "username": "test",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)
