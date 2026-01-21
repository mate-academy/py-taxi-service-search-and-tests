from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_first_name_last_name(self):
        form_data = {
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345",
            "username": "test_username",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
