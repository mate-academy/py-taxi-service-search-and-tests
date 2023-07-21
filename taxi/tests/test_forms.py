from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_first_last_name(self):
        form_data = {
            "username": "testuser",
            "license_number": "ABC12345",
            "first_name": "fime",
            "last_name": "lame",
            "password1": "test12345",
            "password2": "test12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)
