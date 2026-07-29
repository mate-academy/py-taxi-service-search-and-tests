from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
)


class ValidateLicenseNumberTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_wrong_length_raises_error(self):
        with self.assertRaises(Exception):
            validate_license_number("ABC1234")

        with self.assertRaises(Exception):
            validate_license_number("ABC123456")

    def test_license_number_first_3_not_uppercase_raises_error(self):
        with self.assertRaises(Exception):
            validate_license_number("abc12345")

    def test_license_number_first_3_not_letters_raises_error(self):
        with self.assertRaises(Exception):
            validate_license_number("AB112345")

    def test_license_number_last_5_not_digits_raises_error(self):
        with self.assertRaises(Exception):
            validate_license_number("ABC1234A")


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_with_valid_data_is_valid(self):
        form_data = {
            "username": "test.driver",
            "password1": "testpass123qwe",
            "password2": "testpass123qwe",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_driver_creation_form_with_invalid_license_is_invalid(self):
        form_data = {
            "username": "test.driver",
            "password1": "testpass123qwe",
            "password2": "testpass123qwe",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "invalid",
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})

        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})

        self.assertFalse(form.is_valid())
