from unittest import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_correct(self):
        form_data = {
            "username": "ArlaCake",
            "password1": "somepassword123",
            "password2": "somepassword123",
            "first_name": "Arla",
            "last_name": "Cake",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
