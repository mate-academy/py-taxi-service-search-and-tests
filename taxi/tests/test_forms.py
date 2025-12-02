from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form_data = {
            "username": "test",
            "password1": "test123Q123",
            "password2": "test123Q123",
            "license_number": "ABC12345",
            "first_name": "test_first",
            "last_name": "test_last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_number_is_valid(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_number_length(self):
        form_data = {"license_number": "ABC1234"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_last_five_is_digits(self):
        form_data = {"license_number": "ABC123ab"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_first_three_chars(self):
        form_data = {"license_number": "A11123ab"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
