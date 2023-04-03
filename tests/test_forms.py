from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreateFormTests(TestCase):
    def test_user_create(self):
        test_data = {
            "username": "test_user",
            "password1": "qwerty1234q",
            "password2": "qwerty1234q",
            "first_name": "Te",
            "last_name": "St",
            "license_number": "QWE12345"
        }

        form = DriverCreationForm(data=test_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test_data)


class LicenseUpdateFormTest(TestCase):
    def test_update_driver_license(self):
        test = {
            "license_number": "QWE12345",
        }

        form = DriverLicenseUpdateForm(data=test)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test)

    def test_check_valid_license_number(self):
        test_lt_8_characters = DriverLicenseUpdateForm(
            data={"license_number": "QWE"}
        )
        test_gt_8_characters = DriverLicenseUpdateForm(
            data={"license_number": "QWE123456"}
        )
        test_first_3_isupper = DriverLicenseUpdateForm(
            data={"license_number": "qwe12345"}
        )
        test_last_5_isdigit = DriverLicenseUpdateForm(
            data={"license_number": "QWE1234Y"}
        )

        self.assertFalse(test_lt_8_characters.is_valid())
        self.assertFalse(test_gt_8_characters.is_valid())
        self.assertFalse(test_first_3_isupper.is_valid())
        self.assertFalse(test_last_5_isdigit.is_valid())
