from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        """
        Test that driver created with valid data!
        """
        data = {
            "username": "adron",
            "license_number": "ABC12345",
            "first_name": "Andrii",
            "last_name": "Chubenko",
            "password1": "qwerty1234!",
            "password2": "qwerty1234!",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)
