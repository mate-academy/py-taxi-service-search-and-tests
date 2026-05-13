
from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_license_update_form_wrong_license_number(self):
        wrong_licenses = ["URU1235", "uru12345", "URU12U45"]
        for error in wrong_licenses:
            form = DriverLicenseUpdateForm(data={"license_number": error})
            self.assertFalse(form.is_valid())

    def test_driver_creation_form(self):
        form_data = {"username": "test",
                     "password1": "test123test",
                     "password2": "test123test",
                     "first_name": "test",
                     "last_name": "test123test",
                     "license_number": "URU12645"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
