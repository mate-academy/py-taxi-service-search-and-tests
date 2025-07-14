from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_add_fields_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "AAA12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
