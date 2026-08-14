from django.test import TestCase
from taxi.forms import (
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class FormsTests(TestCase):
    def test_driver_search_form_valid_data(self) -> None:
        form_data = {"username": "john_doe"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "john_doe")

    def test_driver_search_form_empty_is_valid(self) -> None:
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid_data(self) -> None:
        form_data = {"model": "Camry"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Camry")

    def test_manufacturer_search_form_valid_data(self) -> None:
        form_data = {"name": "Toyota"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")
