from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_fields_is_valid(self):
        form_data = {
            "username": "test_u",
            "password1": "password_1",
            "password2": "password_1",
            "license_number": "QWE12345",
            "first_name": "test_f",
            "last_name": "test_l",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
