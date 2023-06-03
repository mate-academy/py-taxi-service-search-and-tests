from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm
)


class FormsTests(TestCase):
    def test_driver_creation_added_fields(self):
        driver = {
            "username": "new_yorker",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Woody",
            "last_name": "Allen",
            "license_number": "POW12345"
        }
        form = DriverCreationForm(data=driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, driver)

    def test_license_update_not_8_symb(self):
        license_number = {"license_number": "ABC123456"}
        form = DriverLicenseUpdateForm(license_number)
        self.assertFalse(form.is_valid())
