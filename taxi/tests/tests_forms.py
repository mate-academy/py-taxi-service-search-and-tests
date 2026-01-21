from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_main_fields_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "test2345",
            "password2": "test2345",
            "first_name": "Test First Name",
            "last_name": "Test Last Name",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_license_number_is_no_valid(self):
        form_data = {
            "username": "test",
            "password1": "test2345",
            "password2": "test2345",
            "license_number": "AaA12a456",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
