from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password_12345",
            "password2": "test_password_12345",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "CRE12345"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)
