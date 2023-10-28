from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase

from taxi.forms import (validate_license_number,
                        DriverCreationForm,
                        DriverLicenseUpdateForm)


class ValidateLicenseNumberTest(SimpleTestCase):

    def test_correct_license_number(self) -> None:
        license_number = "ABC12345"
        self.assertEqual(validate_license_number(license_number),
                         license_number)

    def test_license_number_length_less_than_eight(self) -> None:
        incorrect_license_number = "ABC1234"

        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number(incorrect_license_number)

    def test_first_three_symbols_should_be_uppercase_letters(self) -> None:
        incorrect_license_numbers = [
            "12345678",
            "abc12345"
        ]

        for license_number in incorrect_license_numbers:
            with self.assertRaisesMessage(
                    ValidationError,
                    "First 3 characters should be uppercase letters"
            ):
                validate_license_number(license_number)

    def test_last_five_symbols_should_be_digits(self) -> None:
        incorrect_license_number = "ABC2323_"

        with self.assertRaisesMessage(ValidationError,
                                      "Last 5 characters should be digits"):
            validate_license_number(incorrect_license_number)


class DriverCreationFormTest(TestCase):
    base_form_data = {
        "username": "admin.test",
        "password1": "Sjd123siudjnA",
        "password2": "Sjd123siudjnA",
    }

    def test_create_form_with_valid_license_number(self) -> None:
        form_data = self.base_form_data.copy()
        form_data.update(license_number="ABC12345")

        form = DriverCreationForm(form_data)

        self.assertTrue(form.is_valid())

    def test_create_form_without_license_number(self) -> None:
        form = DriverCreationForm(self.base_form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form,
                             "license_number",
                             "This field is required.")

    def test_create_form_with_license_number_length_lt_eight(self) -> None:
        form_data = self.base_form_data.copy()
        form_data.update(license_number="ABC1234")

        form = DriverCreationForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form,
                             "license_number",
                             "License number should consist of 8 characters")

    def test_create_form_with_incorrect_first_three_symbols(self) -> None:
        incorrect_license_numbers = [
            "12345678",
            "abc12345"
        ]

        for license_number in incorrect_license_numbers:
            form_data = self.base_form_data.copy()
            form_data.update(license_number=license_number)

            form = DriverCreationForm(form_data)

            self.assertFalse(form.is_valid())
            self.assertFormError(
                form,
                "license_number",
                "First 3 characters should be uppercase letters"
            )

    def test_create_form_with_incorrect_last_five_symbols(self) -> None:
        form_data = self.base_form_data.copy()
        form_data.update(license_number="ABC1234A")

        form = DriverCreationForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form,
                             "license_number",
                             "Last 5 characters should be digits")


class DriverLicenseUpdateFormTest(TestCase):

    def test_update_form_with_valid_license_number(self) -> None:
        form_data = {"license_number": "ABC12345"}

        form = DriverLicenseUpdateForm(form_data)

        self.assertTrue(form.is_valid())

    def test_create_form_without_license_number(self) -> None:
        form = DriverLicenseUpdateForm({})

        self.assertFalse(form.is_valid())
        self.assertFormError(form,
                             "license_number",
                             "This field is required.")

    def test_create_form_with_license_number_length_lt_eight(self) -> None:
        form_data = {"license_number": "ABC1234"}
        form = DriverLicenseUpdateForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form,
                             "license_number",
                             "License number should consist of 8 characters")

    def test_create_form_with_incorrect_first_three_symbols(self) -> None:
        incorrect_license_numbers = [
            "12345678",
            "abc12345"
        ]

        for license_number in incorrect_license_numbers:
            form_data = {"license_number": license_number}
            form = DriverLicenseUpdateForm(form_data)

            self.assertFalse(form.is_valid())
            self.assertFormError(
                form,
                "license_number",
                "First 3 characters should be uppercase letters"
            )

    def test_create_form_with_incorrect_last_five_symbols(self) -> None:
        form_data = {"license_number": "ABC1234A"}
        form = DriverLicenseUpdateForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form,
                             "license_number",
                             "Last 5 characters should be digits")
