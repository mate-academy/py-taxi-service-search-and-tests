from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class DriverLicenseUpdateFormTest(TestCase):
    def test_invalid_length_license_number(self):
        form_data = {
            "license_number": "MORETHAN8"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_upper_letters_quantity(self):
        form_data = {
            "license_number": "MORE1234"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_digits_quantity(self):
        form_data = {
            "license_number": "MOR1234"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_license_number(self):
        form_data = {
            "license_number": "ADM56984"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )


class DriverCreationFormTest(TestCase):
    """Added additional fields: first_name, last_name, license_number"""

    def test_valid_data(self):
        form_data = {
            "username": "Bob4ik123",
            "password1": "Bobapass123!",
            "password2": "Bobapass123!",
            "first_name": "Bob",
            "last_name": "Bambuko",
            "license_number": "PSV12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
