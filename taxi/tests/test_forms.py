from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_form_is_valid(self):
        form_data = {
            "username": "maxitoska",
            "password1": "3134maxim",
            "password2": "3134maxim",
            "first_name": "Maksym",
            "last_name": "Melnyk",
            "license_number": "JKQ12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_form_is_not_valid(self):
        form_data = {
            "username": "maxitoska",
            "password1": "31",
            "password2": "31",
            "first_name": "Maksym",
            "last_name": "Melnyk",
            "license_number": "JK12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
