from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_valid_data(self):
        form_data = {
            "username": "test_user",
            "password1": "778899oo",
            "password2": "778899oo",
            "first_name": "First Name",
            "last_name": "Last Name",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_change_invalid_license_number(self):
        license_numbers = ["AAA123445", "AaA12345", "A5"]

        for license_number in license_numbers:
            with self.subTest(amount=license_number):
                form = DriverLicenseUpdateForm(data={
                    "license_number": license_number
                })

                self.assertFalse(form.is_valid())
