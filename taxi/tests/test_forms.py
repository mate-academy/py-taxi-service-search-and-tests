from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "username_test",
            "password1": "user_password_test",
            "password2": "user_password_test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "QWE12345"
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_driver_creation_form_license_number_first_last_name_valid(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)

    def test_driver_creation_form_license_number_longer_then_expected(self):
        self.form_data["license_number"] = "QWE123451"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)

    def test_driver_creation_form_license_number_shorter_then_expected(self):
        self.form_data["license_number"] = "QWE1234"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)

    def test_driver_creation_form_license_number_not_three_chars(self):
        self.form_data["license_number"] = "QW112341"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)

    def test_driver_creation_form_license_number_not_five_digits(self):
        self.form_data["license_number"] = "QWE11234I"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)

    def test_driver_creation_form_license_number_not_upper_chars(self):
        self.form_data["license_number"] = "qwe112341"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)
