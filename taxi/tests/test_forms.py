from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class DriverLicenseUpdateFormTest(TestCase):
    def test_invalid_length_license_number(self):
        form_data = {
            "license_number": "ASVERTY11"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_upper_letters_quantity(self):
        form_data = {
            "license_number": "BVNC0987"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_digits_quantity(self):
        form_data = {
            "license_number": "IDW1234"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_license_number(self):
        form_data = {
            "license_number": "ABD76531"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )


class DriverCreationFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            "username": "Test123",
            "password1": "DriverTesting123!",
            "password2": "DriverTesting123!",
            "first_name": "Test",
            "last_name": "lastTest",
            "license_number": "AAA12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
