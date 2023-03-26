from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "pass688uJH",
            "password2": "pass688uJH",
            "license_number": "FRG54345",
            "first_name": "Test First",
            "last_name": "Test Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
