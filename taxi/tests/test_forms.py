from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_user",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Firsttest",
            "last_name": "Lasttest",
            "license_number": "ADM56984",
        }

    def test_driver_form_with_license_number_first_last_name_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_update_form_validation_license_number(self):
        """
        License number should consist of 8 characters
        First 3 characters should be uppercase letters
        Last 5 characters should be digits
        """
        self.form_data["license_number"] = "ADM569846"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data["license_number"] = "adm56984"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data["license_number"] = "1D556984"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data["license_number"] = "ADMF698"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
