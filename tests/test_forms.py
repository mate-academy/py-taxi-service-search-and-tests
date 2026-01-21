from unittest import TestCase
from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form_pseudonym_is_valid(self) -> None:
        form_data = {
            "username": "new_user",
            "password1": "usertest174",
            "password2": "usertest174",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "Test number",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
