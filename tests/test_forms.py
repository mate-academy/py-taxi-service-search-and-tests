from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class TestDriverForm(TestCase):
    def test_driver_creation_form(self):
        user_info = {
            "username": "Voldemort",
            "password1": "ban12345",
            "password2": "ban12345",
            "first_name": "Tom",
            "last_name": "Riddle",
            "license_number": "ZXC12345"
        }
        form = DriverCreationForm(data=user_info)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, user_info)

    def test_update_driver_license_len(self):
        license_number = {"license_number": "123456789"}
        form = DriverLicenseUpdateForm(data=license_number)

        self.assertFalse(form.is_valid())

    def test_update_driver_license_first_3(self):
        license_number = {"license_number": "ab123456"}
        form = DriverLicenseUpdateForm(data=license_number)

        self.assertFalse(form.is_valid())

    def test_update_driver_license_last_5(self):
        license_number = {"license_number": "ABCD2345"}
        form = DriverLicenseUpdateForm(data=license_number)

        self.assertFalse(form.is_valid())
