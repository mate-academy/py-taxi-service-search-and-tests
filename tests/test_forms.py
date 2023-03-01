from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreateFormTests(TestCase):
    def test_driver_create_with_license_first_name_last_name(self):
        form_data = {
            "license_number": "ABC12345",
            "username": "jimmy.beam",
            "first_name": "Jimmy",
            "last_name": "Beam",
            "password1": "user1234",
            "password2": "user1234"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTests(TestCase):
    def test_update_driver_license(self):
        test_driver = {
            "license_number": "ABC12345",
        }

        form = DriverLicenseUpdateForm(data=test_driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, test_driver)

    def test_check_valid_license_number(self):
        test_characters = DriverLicenseUpdateForm(
            data={"license_number": "ABC123"}
        )
        test_first_3_letter = DriverLicenseUpdateForm(
            data={"license_number": "AB912345"}
        )
        test_last_5_digits = DriverLicenseUpdateForm(
            data={"license_number": "ABC123F55"}
        )

        self.assertFalse(test_characters.is_valid())
        self.assertFalse(test_first_3_letter.is_valid())
        self.assertFalse(test_last_5_digits.is_valid())
