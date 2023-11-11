from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormsTest(TestCase):

    def test_driver_create_form(self):
        form_data = {
            "username": "test_username",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "license_number": "WWW11111",
            "first_name": "test_test",
            "last_name": "test_test_test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
