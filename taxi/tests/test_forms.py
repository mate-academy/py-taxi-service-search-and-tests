from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverFormTests(TestCase):
    def setUp(self):
        self.driver = {
            "username": "user",
            "password1": "PASSWORD_pass_123",
            "password2": "PASSWORD_pass_123",
            "first_name": "firstname",
            "last_name": "Lastname",
            "license_number": "ABC12345"
        }

    def test_driver_creation_form(self):
        form = DriverCreationForm(data=self.driver)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.driver)

    def test_driver_creation_form_blank_license_number(self):
        self.driver["license_number"] = ""
        form = DriverCreationForm(data=self.driver)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.valid_license_number = "ABC12345"
        self.invalid_license_number_short = "ABC1234"
        self.invalid_license_number_long = "ABC123456"
        self.invalid_license_number_non_alpha = "123ABC45"
        self.invalid_license_number_non_digit = "ABC12ERR"

    def test_driver_license_update_form_valid(self):
        data = {"license_number": self.valid_license_number}
        form = DriverLicenseUpdateForm(data=data)

        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_short_license_number(self):
        data = {"license_number": self.invalid_license_number_short}
        form = DriverLicenseUpdateForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_invalid_to_long_license_number(self):
        data = {"license_number": self.invalid_license_number_long}
        form = DriverLicenseUpdateForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_invalid_no_alpha_license_number(self):
        data = {"license_number": self.invalid_license_number_non_alpha}
        form = DriverLicenseUpdateForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_invalid_no_digit_license_number(self):
        data = {"license_number": self.invalid_license_number_non_digit}
        form = DriverLicenseUpdateForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
