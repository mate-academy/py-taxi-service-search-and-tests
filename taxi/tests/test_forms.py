from django.test import TestCase

from taxi.forms import DriverForm, DriverLicenseUpdateForm


class FormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "$h9wD2qm",
            "password2": "$h9wD2qm",
        }

    def test_driver_form_valid_when_driver_license_valid(self) -> None:
        self.form_data["license_number"] = "ABC12345"
        form = DriverForm(self.form_data)

        self.assertTrue(form.is_valid())

    def test_driver_form_invalid_when_driver_license_length_is_greater_then_8(
        self,
    ) -> None:
        self.form_data["license_number"] = "ABC123456"
        form = DriverForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_driver_form_invalid_when_driver_license_length_is_less_then_8(
        self,
    ) -> None:
        self.form_data["license_number"] = "ABC1234"
        form = DriverForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_driver_form_invalid_when_first_3_characters_are_not_uppercase(
        self,
    ) -> None:
        self.form_data["license_number"] = "Abc12345"
        form = DriverForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_driver_form_invalid_when_first_3_characters_are_not_letters(
        self,
    ) -> None:
        self.form_data["license_number"] = "Ab123456"
        form = DriverForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_driver_form_invalid_when_last_5_characters_are_not_digits(
        self,
    ) -> None:
        self.form_data["license_number"] = "ABC123k5"
        form = DriverForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_license_form_valid_when_driver_license_valid(self) -> None:
        self.form_data["license_number"] = "ABC12345"
        form = DriverLicenseUpdateForm(self.form_data)

        self.assertTrue(form.is_valid())

    def test_license_form_invalid_when_driver_license_length_is_greater_then_8(
        self,
    ) -> None:
        self.form_data["license_number"] = "ABC123456"
        form = DriverLicenseUpdateForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_license_form_invalid_when_driver_license_length_is_less_then_8(
        self,
    ) -> None:
        self.form_data["license_number"] = "ABC1234"
        form = DriverLicenseUpdateForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_license_form_invalid_when_first_3_characters_are_not_uppercase(
        self,
    ) -> None:
        self.form_data["license_number"] = "Abc12345"
        form = DriverLicenseUpdateForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_license_form_invalid_when_first_3_characters_are_not_letters(
        self,
    ) -> None:
        self.form_data["license_number"] = "Ab123456"
        form = DriverLicenseUpdateForm(self.form_data)

        self.assertFalse(form.is_valid())

    def test_license_form_invalid_when_last_5_characters_are_not_digits(
        self,
    ) -> None:
        self.form_data["license_number"] = "ABC123k5"
        form = DriverLicenseUpdateForm(self.form_data)

        self.assertFalse(form.is_valid())
