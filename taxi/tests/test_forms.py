from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name(self):
        form_data = {
            "username": "lewis.hamilton",
            "password1": "12password34",
            "password2": "12password34",
            "first_name": "Lewis",
            "last_name": "Hamilton",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
