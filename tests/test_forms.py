from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTest(TestCase):
    data = {
        "username": "UserTester",
        "first_name": "FirstName",
        "last_name": "LastName",
        "password1": "1qazcde3",
        "password2": "1qazcde3",
        "license_number": "ABC12345"
    }

    def test_user_form(self):
        form = DriverCreationForm(data=self.data)

        self.assertTrue(form.is_valid())


class LicenseUpdateFormTest(TestCase):
    def test_license_len_is_8(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC123456"}
        )

        self.assertFalse(form.is_valid())

    def test_license_startswith_letters(self):
        form_with_lowercase = DriverLicenseUpdateForm(
            data={"license_number": "abc12345"}
        )
        form_without_letters = DriverLicenseUpdateForm(
            data={"license_number": "12345678"}
        )
        form_with_a_lot_of_letters_lol = DriverLicenseUpdateForm(
            data={"license_number": "ABCD2345"}
        )
        form_with_less_letters = DriverLicenseUpdateForm(
            data={"license_number": "AB012345"}
        )

        self.assertFalse(form_with_lowercase.is_valid())
        self.assertFalse(form_without_letters.is_valid())
        self.assertFalse(form_with_a_lot_of_letters_lol.is_valid())
        self.assertFalse(form_with_less_letters.is_valid())
