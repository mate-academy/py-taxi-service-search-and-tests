from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTest(TestCase):

    def test_driver_creation_form(self):
        form_data = {
            "username": "testuser",
            "password1": "passwww123",
            "password2": "passwww123",
            "first_name": "Ivan",
            "last_name": "Testovuy",
            "license_number": "TAS11234"
        }

        form = DriverCreationForm(data=form_data)
        self.assert_(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_chars(self):
        form_data = {"license_number": "AsD12345"}
        form = DriverCreationForm(form_data)

        self.assertFalse(form.is_valid())

    def test_driver_creation_form_len(self):
        form_data = {"license_number": "AAD1234522222"}
        form = DriverCreationForm(form_data)

        self.assertFalse(form.is_valid())

    def test_driver_creation_form_digits(self):
        form_data = {"license_number": "ADD21a22"}
        form = DriverCreationForm(form_data)

        self.assertFalse(form.is_valid())

    def test_driver_update_license_number_form_chars(self):
        form_date = {"license_number": "AsA12345"}
        form = DriverLicenseUpdateForm(form_date)

        self.assertFalse(form.is_valid())

    def test_driver_update_license_number_form_len(self):
        form_date = {"license_number": "AAA12342225"}
        form = DriverLicenseUpdateForm(form_date)

        self.assertFalse(form.is_valid())

    def test_driver_update_license_number_form_digits(self):
        form_date = {"license_number": "AAA12a42"}
        form = DriverLicenseUpdateForm(form_date)

        self.assertFalse(form.is_valid())
