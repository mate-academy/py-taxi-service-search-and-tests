from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password1234",
            "password2": "test_password1234",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "WWW12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form(self):
        form_data = {"license_number": "WWW54321"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
