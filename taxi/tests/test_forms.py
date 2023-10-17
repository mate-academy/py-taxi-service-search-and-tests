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

    def test_driver_creation_form_is_valid(self) -> None:
        form = DriverCreationForm(self.form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data, self.form_data)

    def test_should_be_invalid_when_len_of_license_number_is_not_8(
            self
    ) -> None:
        self.form_data["license_number"] = "123456"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_first_3_should_be_in_uppercase_letters(self) -> None:
        self.form_data["license_number"] = "abc123456"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_last_5_characters_should_be_digits(self) -> None:
        self.form_data["license_number"] = "12345ABC"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_update_form_is_valid(self) -> None:
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_should_be_invalid_when_len_of_license_number_is_not_8(
            self
    ) -> None:
        form_data = {"license_number": "123456"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_first_3_should_be_in_uppercase_letters(self) -> None:
        form_data = {"license_number": "abc123456"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_last_5_characters_should_be_digits(self) -> None:
        form_data = {"license_number": "12345ABC"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
