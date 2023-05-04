from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_user",
            "password1": "passtest123",
            "password2": "passtest123",
            "first_name": "Ivan",
            "last_name": "Testovuy",
            "license_number": "TES11234"
        }
        form = DriverCreationForm(data=form_data)
        self.assert_(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_driver_creation_form_len(self):
        form_data = {"license_number": "TES112341"}
        form = DriverCreationForm(form_data)
        self.assertFalse(form.is_valid())

    def test_validate_driver_creation_form_chars(self):
        form_data = {"license_number": "TsS112341"}
        form = DriverCreationForm(form_data)
        self.assertFalse(form.is_valid())

    def test_validate_driver_creation_form_digs(self):
        form_data = {"license_number": "TsSs12341"}
        form = DriverCreationForm(form_data)
        self.assertFalse(form.is_valid())

    def test_validate_driver_license_update_form_len(self):
        form_data = {"license_number": "TES112341"}
        form = DriverLicenseUpdateForm(form_data)
        self.assertFalse(form.is_valid())

    def test_validate_driver_license_update_form_chars(self):
        form_data = {"license_number": "TsS112341"}
        form = DriverLicenseUpdateForm(form_data)
        self.assertFalse(form.is_valid())

    def test_validate_driver_license_update_form_digs(self):
        form_data = {"license_number": "TsSs12341"}
        form = DriverLicenseUpdateForm(form_data)
        self.assertFalse(form.is_valid())
