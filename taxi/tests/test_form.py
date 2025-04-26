from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form_license_number_first_and_last_name(self):
        form_data = {
            "username": "test_user",
            "password1": "test 1234",
            "password2": "test 1234",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )

    def test_driver_update_license_number(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
