from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class DriverFormTests(TestCase):
    def test_valid_license_number(self):
        license_number = "ASD34510"

        self.assertTrue(
            validate_license_number(license_number),
            license_number
        )

    def test_driver_creation_form_with_license_number_first_name_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user98765",
            "password2": "user98765",
            "first_name": "First test",
            "last_name": "Last test",
            "license_number": "ADD99999"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
