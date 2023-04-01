from django.test import TestCase
from taxi.forms import DriverLicenseUpdateForm


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_license(self) -> None:
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_numbers(self) -> None:
        form_data = {"license_number": "12345678"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {"license_number": "ABC123456"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {"license_number": "abc12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
