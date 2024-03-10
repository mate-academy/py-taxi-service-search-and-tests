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
            "username": "test",
            "password1": "test123123",
            "password2": "test123123",
            "first_name": "Bob",
            "last_name": "Marley",
            "license_number": "BMC12345",
        }

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
