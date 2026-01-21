from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "new_user",
            "password1": "test123user",
            "password2": "test123user",
            "license_number": "NUM12345",
            "first_name": "Test First",
            "last_name": "Test Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
