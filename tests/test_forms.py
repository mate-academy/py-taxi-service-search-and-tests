from django.test import TestCase

from taxi.forms import DriverCreationForm


class CreationOrUpdateFormTest(TestCase):
    def setUp(self) -> None:
        password = "TestPass123"
        self.form_data = {
            "username": "Kirontiko",
            "password1": password,
            "password2": password,
            "license_number": "AAA12345",
            "first_name": "John",
            "last_name": "Smith"
        }

    def test_driver_creation_form_with_license_number_valid(self):

        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_license_number_len_not_equal_8(self):
        self.form_data["license_number"] = "AAA123456789"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_license_number_not_starts_with_3_chars(
            self):
        self.form_data["license_number"] = "12345678"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_license_number_not_ends_with_5_digits(
            self):
        self.form_data["license_number"] = "AAAA1234"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_update_form_with_license_number_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_driver_update_form_with_license_number_invalid(self):
        self.form_data["license_number"] = "AAAA1234135"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
