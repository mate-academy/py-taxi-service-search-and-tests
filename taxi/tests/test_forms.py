from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class DriverLicenseUpdateFormTests(TestCase):
    def test_license_number_valid(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"}
        )

        self.assertTrue(form.is_valid())

    def test_license_first_3_chars_uppercase(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "abc12345"}
        )

        self.assertFalse(form.is_valid())

    def test_license_number_last_five_chars_should_be_digits(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABCABCDE"}
        )

        self.assertFalse(form.is_valid())

    def test_license_number_should_have_8_characters(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC1234"}
        )

        self.assertFalse(form.is_valid())
