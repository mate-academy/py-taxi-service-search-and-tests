from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormTest(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "Qwer123456",
            "password2": "Qwer123456",
            "first_name": "test first name",
            "last_name": "test last name",
            "license_number": "QWE12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
