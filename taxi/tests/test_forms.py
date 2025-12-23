from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "TestDriver",
            "first_name": "Test First",
            "last_name": "Test Last",
            "password1": "TestPassword 123",
            "password2": "TestPassword 123",
            "license_number": "NTS12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
