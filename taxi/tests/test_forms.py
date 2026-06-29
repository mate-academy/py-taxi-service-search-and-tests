from django.core.exceptions import ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from django.test import TestCase

from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    validate_license_number,
)


class CarFormTest(TestCase):
    def test_car_form_fields(self) -> None:
        form = CarForm()

        self.assertEqual(
            list(form.fields.keys()),
            ["model", "manufacturer", "drivers"],
        )

    def test_car_form_drivers_uses_checkbox_widget(self) -> None:
        form = CarForm()

        self.assertIsInstance(
            form.fields["drivers"].widget,
            CheckboxSelectMultiple,
        )


class DriverCreationFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_username",
            "password1": "pass12345",
            "password2": "pass12345",
            "license_number": "ABC12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }

    def test_driver_creation_form_fields(self) -> None:
        form = DriverCreationForm()

        self.assertEqual(
            list(form.fields.keys()),
            [
                "username",
                "license_number",
                "first_name",
                "last_name",
                "password1",
                "password2",
            ],
        )

    def test_driver_creation_form_valid_license_number(self) -> None:
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number_length(
            self,
    ) -> None:
        self.form_data["license_number"] = "ABC1234"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_data()["license_number"][0].message,
            "License number should consist of 8 characters",
        )

    def test_driver_creation_form_invalid_license_first_3_not_uppercase(
            self,
    ) -> None:
        self.form_data["license_number"] = "abc12345"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_data()["license_number"][0].message,
            "First 3 characters should be uppercase letters",
        )

    def test_driver_creation_form_invalid_license_last_5_not_digits(
            self,
    ) -> None:
        self.form_data["license_number"] = "ABC45abc"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_data()["license_number"][0].message,
            "Last 5 characters should be digits",
        )


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_fields(self) -> None:
        form = DriverLicenseUpdateForm()

        self.assertEqual(
            list(form.fields.keys()),
            ["license_number"],
        )

    def test_driver_license_update_form_valid_license_number(self) -> None:
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"},
        )

        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_license_length(
            self,
    ) -> None:
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC1234"},
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_data()["license_number"][0].message,
            "License number should consist of 8 characters",
        )

    def test_driver_license_update_invalid_first_3_not_uppercase(
            self,
    ) -> None:
        form = DriverLicenseUpdateForm(
            data={"license_number": "abc12345"},
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_data()["license_number"][0].message,
            "First 3 characters should be uppercase letters",
        )

    def test_driver_license_update_invalid_last_5_not_digits(
            self,
    ) -> None:
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABCabc45"},
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_data()["license_number"][0].message,
            "Last 5 characters should be digits",
        )


class ValidateLicenseNumberFunctionTest(TestCase):
    def test_validate_license_number_valid(self) -> None:
        license_number = "ABC12345"

        self.assertEqual(
            validate_license_number(license_number),
            license_number,
        )

    def test_validate_license_number_invalid_length(self) -> None:
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters",
        ):
            validate_license_number("ABC1234")

    def test_validate_license_number_invalid_first_3_not_uppercase(
            self,
    ) -> None:
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters",
        ):
            validate_license_number("abc12345")

    def test_validate_license_number_invalid_last_5_not_digits(
            self,
    ) -> None:
        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits",
        ):
            validate_license_number("ABCabc45")


class SearchFormsTest(TestCase):
    def test_driver_search_form_username_field_not_required(
            self
    ) -> None:
        form = DriverSearchForm()

        self.assertFalse(form.fields["username"].required)

    def test_car_search_form_model_field_not_required(
            self
    ) -> None:
        form = CarSearchForm()

        self.assertFalse(form.fields["model"].required)

    def test_manufacturer_search_form_name_field_not_required(
            self
    ) -> None:
        form = ManufacturerSearchForm()

        self.assertFalse(form.fields["name"].required)

    def test_driver_search_form_empty_data_is_valid(
            self
    ) -> None:
        form = DriverSearchForm(data={})

        self.assertTrue(form.is_valid())

    def test_car_search_form_empty_data_is_valid(
            self
    ) -> None:
        form = CarSearchForm(data={})

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_empty_data_is_valid(
            self
    ) -> None:
        form = ManufacturerSearchForm(data={})

        self.assertTrue(form.is_valid())
