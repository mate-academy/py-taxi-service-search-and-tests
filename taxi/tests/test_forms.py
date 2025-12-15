from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "Test",
            "password1": "Qwrd.231",
            "password2": "Qwrd.231",
            "first_name": "First",
            "last_name": "Second",
            "license_number": "QWE45678",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["password1"],
            form_data["password1"]
        )
        self.assertEqual(
            form.cleaned_data["password2"],
            form_data["password2"]
        )

    def test_driver_creation_form_validation(self):
        form_data = {
            "username": "Test",
            "password1": "Qwrd.231",
            "password2": "Qwrd.231",
            "first_name": "First",
            "last_name": "Second",
            "license_number": "LETTERSS",
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "QWE456789"

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "QWE4567"

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "12345678"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "123QWERT"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
