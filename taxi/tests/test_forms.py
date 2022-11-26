from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "newuser",
            "password1": "u123test",
            "password2": "u123test",
            "first_name": "Nametest",
            "last_name": "Surnametest",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
        self.assertEqual(form.fields.keys(), form_data.keys())

    def test_driver_license_update_form(self):
        form_data = {"license_number": "AAA12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
        self.assertEqual(form.fields.keys(), form_data.keys())

    def test_driver_license_update_form_with_invalid_data(self):
        form_data = {"license_number": "A12A1F2345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
        self.assertNotEqual(form.fields.keys(), form_data.keys())
