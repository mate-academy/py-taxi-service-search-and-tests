from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_new_fields(self):
        form_data = {
            "username": "new_user",
            "password1": "WWee123456",
            "password2": "WWee123456",
            "first_name": "test_firstname",
            "last_name": "test_lastname",
            "license_number": "WWW12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
