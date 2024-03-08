from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class TestForms(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_user",
            "password1": "v_pl_BI8518AI",
            "password2": "v_pl_BI8518AI",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "ABC12345",
        }

    def test_driver_creation_form_with_additional_fields(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_invalid_license(self) -> None:
        for license_number in (
                "abc12345",
                "123qwerty",
                "ABC123456",
                "ABCqwert"
        ):
            self.form_data["license_number"] = license_number
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())

    def test_manufacturer_search_form(self) -> None:
        form = ManufacturerSearchForm(data={"name": "test_name"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test_name")

    def test_car_search_form(self) -> None:
        form = CarSearchForm(data={"model": "test_model"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test_model")

    def test_driver_search_form(self) -> None:
        form = DriverSearchForm(data={"username": "test_username"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test_username")
