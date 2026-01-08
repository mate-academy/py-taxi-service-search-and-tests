from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_tester1",
            "password1": "user336test",
            "password2": "user336test",
            "first_name": "test",
            "last_name": "user",
            "license_number": "FFG82821"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )

        form_data = {
            "username": "test_tester1",
            "password1": "user336test",
            "password2": "user336test",
            "first_name": "test",
            "last_name": "user",
            "license_number": "FFG8221"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "FF82821"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "license_number": "FF82821412@"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "license_number": "FFA82821"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
