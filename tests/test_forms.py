from unittest import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm
)


class DriverFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "petro",
            "first_name": "Petro Chur",
            "last_name": "Petro Chur Petrovych",
            "license_number": "SSS32121",
            "password1": "test_password123",
            "password2": "test_password123",
        }

    def test_driver_create_form_with_licence_num_is_valid(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_validate_license_number_when_len_not_eq_8(self) -> None:
        self.form_data["license_number"] = "SSS555666"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_validate_license_number_when_starts_with_wrong_char(self) -> None:
        self.form_data["license_number"] = "maruska123"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_validate_license_number_when_ends_with_wrong_chars(self) -> None:
        self.form_data["license_number"] = "WWB5544ou"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class TestDriverUsernameSearchForm(TestCase):
    def test_driver_username_search_form(self) -> None:
        form = DriverUsernameSearchForm(
            data={"username": "test"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test")


class TestCarModelSearchForm(TestCase):
    def test_car_model_search_form(self) -> None:
        form = CarModelSearchForm(
            data={"model": "Test Model"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Test Model")


class TestManufacturerNameSearchForm(TestCase):
    def test_manufacturer_model_search_form(self) -> None:
        form = ManufacturerNameSearchForm(
            data={"name": "Test Name"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test Name")
