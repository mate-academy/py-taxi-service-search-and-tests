from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation(self):
        form_data = {
            "username": "new_driver",
            "password1": "testpassw0rd",
            "password2": "testpassw0rd",
            "first_name": "testfirst",
            "last_name": "testlast",
            "license_number": "QWE12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
