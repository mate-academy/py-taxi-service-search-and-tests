from django.test import TestCase
from django import forms

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturesSearchForm,
    DriversSearchForm,
    CarsSearchForm
)


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.driver_form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "USR11111",
        }

        self.form = DriverCreationForm(data=self.driver_form_data)

    @staticmethod
    def license_form(number: str):
        return DriverLicenseUpdateForm(
            data={"license_number": number}
        )

    def test_driver_creation_form_is_valid(self) -> None:
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.driver_form_data)

    def test_license_number_is_valid(self) -> None:
        self.assertTrue(self.license_form("XWE12345").is_valid())

    def test_length_of_license_number_not_less_than_8(self) -> None:
        self.assertFalse(self.license_form("WE1234").is_valid())

    def test_length_of_license_number_not_more_than_8(self) -> None:
        self.assertFalse(self.license_form("USR1234561").is_valid())

    def test_first_3_characters_are_uppercase_letters(self) -> None:
        self.assertFalse(self.license_form("eDF123456").is_valid())

    def test_last_5_characters_are_digits(self) -> None:
        self.assertFalse(self.license_form("QWEC2345").is_valid())


class TestSearchForms(TestCase):
    @staticmethod
    def get_search_form_by_name(form: str) -> forms.Form:
        test_name = "test field name"
        form_variables = {
            "manufacturer": ManufacturesSearchForm(data={"name": test_name}),
            "car": CarsSearchForm(data={"model": test_name}),
            "driver": DriversSearchForm(data={"username": test_name})

        }
        return form_variables[f"{form}"]

    def test_driver_search_form(self) -> None:
        self.assertTrue(self.get_search_form_by_name("driver").is_valid())

    def test_manufacturer_search_form(self) -> None:
        self.assertTrue(
            self.get_search_form_by_name("manufacturer").is_valid()
        )

    def test_car_search_form(self) -> None:
        self.assertTrue(self.get_search_form_by_name("car"))
