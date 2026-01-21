from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "Test123as",
            "password2": "Test123as",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "TES12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
