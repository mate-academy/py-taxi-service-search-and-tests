from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_driver_creation_form_with_additional_fields(self):
        form_data = {
            "username": "test_user",
            "password1": "us3r12t@st@new",
            "password2": "us3r12t@st@new",
            "license_number": "AAA55555",
            "first_name": "Test First",
            "last_name": "Test Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
