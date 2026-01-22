from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_first_last_is_valid(self):
        form_data = {
            "username": "user",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "first_name": "first",
            "last_name": "last",
            "license_number": "ABC12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data, form_data)

    def test_update_license_form_if_one_letter(self):
        form_data = {"license_number": "A12345"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_update_license_form_if_four_digits(self):
        form_data = {"license_number": "ABC1234"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_update_license_form_if_char_more_than_eight(self):
        form_data = {"license_number": "ABCD123456"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_update_license_form_is_valid(self):
        form_data = {"license_number": "ABC12345"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
