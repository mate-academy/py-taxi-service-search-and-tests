from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_with_valid_data(self) -> None:
        form_data = {
            "username": "newuser",
            "password1": "T@xiDrive42",
            "password2": "T@xiDrive42",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "DBA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
