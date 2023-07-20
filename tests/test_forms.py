from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
)


class DriverCreationFormTest(TestCase):
    data = {
        "username": "usertest",
        "first_name": "UserFirst",
        "last_name": "UserLast",
        "password1": "1Qazxrw@",
        "password2": "1Qazxrw@",
        "license_number": "JPN13248"
    }

    def test_success_user_creation(self):
        form = DriverCreationForm(data=self.data)
        form.save()
        self.assertTrue(form.is_valid())


class LicenseUpdateFormTest(TestCase):
    def test_fail_if_license_len_not_valid(self):
        form_too_few_numbers = DriverLicenseUpdateForm(
            data={"license_number": "JPN13"}
        )
        form_too_much_numbers = DriverLicenseUpdateForm(
            data={"license_number": "JPN1324899"}
        )

        self.assertFalse(form_too_few_numbers.is_valid())
        self.assertFalse(form_too_much_numbers.is_valid())

    def test_fail_if_license_letters_not_valid(self):
        form_lowercase = DriverLicenseUpdateForm(
            data={"license_number": "jpn13248"}
        )
        form_without_letters = DriverLicenseUpdateForm(
            data={"license_number": "13248999"}
        )
        form_many_letters = DriverLicenseUpdateForm(
            data={"license_number": "JPNP3248"}
        )
        form_less_letters = DriverLicenseUpdateForm(
            data={"license_number": "JP113248"}
        )

        self.assertFalse(form_lowercase.is_valid())
        self.assertFalse(form_without_letters.is_valid())
        self.assertFalse(form_many_letters.is_valid())
        self.assertFalse(form_less_letters.is_valid())
