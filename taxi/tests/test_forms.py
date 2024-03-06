from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "license_number": "ABC12345",
        }

    def test_should_be_invalid_when_lenght_of_license_is_not_8(self) -> None:
        self.form_data["license_number"] = "123123123"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"],
        )

    def test_first_3_characters_are_not_uppercase_letters(
        self,
    ) -> None:
        self.form_data["license_number"] = "12345678"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"],
        )

    def test_last_5_characters_are_not_digits(
        self,
    ) -> None:
        self.form_data["license_number"] = "ABCabcab"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits", form.errors["license_number"]
        )

    def test_should_be_passed_when_conditions_are_satisfied(self) -> None:
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_should_be_invalid_when_lenght_of_license_is_not_8(self):
        form_data = {"license_number": "123456789"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"],
        )

    def test_first_3_characters_are_not_uppercase_letters(
        self,
    ):
        form_data = {"license_number": "12345678"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"],
        )

    def test_should_be_invalid_when_last_5_characters_are_not_digits(self):
        form_data = {"license_number": "ABCabcab"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits", form.errors["license_number"]
        )

    def test_should_be_passed_when_conditions_are_satisfied(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
