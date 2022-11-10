from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_form_is_valid(self):
        form_data = {
            "username": "sandychicks",
            "password1": "123ichick",
            "password2": "123ichick",
            "first_name": "Sandy",
            "last_name": "Chicks",
            "license_number": "JKQ12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_form_is_not_valid(self):
        form_data = {
            "username": "sandychicks",
            "password1": "12",
            "password2": "12",
            "first_name": "Sandy",
            "last_name": "Chicks",
            "license_number": "JK12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
