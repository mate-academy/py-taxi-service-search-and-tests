from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(
        self,
    ):
        form_data = {
            "username": "user_new",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_valid_license_number(self):
        valid_license_number = "ABC12345"
        form_data = {"license_number": valid_license_number}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"], valid_license_number
        )

    def test_invalid_license_number_length(self):
        invalid_license_number = "ABC123"
        form_data = {"license_number": invalid_license_number}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_invalid_license_number_format(self):
        invalid_license_number = "12345ABC"
        form_data = {"license_number": invalid_license_number}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
