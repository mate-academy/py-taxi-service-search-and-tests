from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    @staticmethod
    def get_form_data() -> dict:
        return {
            "username": "papajoe",
            "password1": "$ecreT_550",
            "password2": "$ecreT_550",
        }

    def test_driver_creation_form_valid_license(self):
        form_data = self.get_form_data()
        form_data["license_number"] = "MAN99901"
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_no_license(self):
        form_data = self.get_form_data()
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_license_incorrect_format(self):
        incorrect_licenses = ["man999", "MAN9999W", "mAN", "1244425f"]
        form_data = self.get_form_data()

        for incorrect_license in incorrect_licenses:
            form_data["license_number"] = incorrect_license
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
