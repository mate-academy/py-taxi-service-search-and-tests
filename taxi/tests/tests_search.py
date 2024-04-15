from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class CarSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = CarSearchForm(data={"model": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form = CarSearchForm()
        self.assertFalse(form.is_valid())


class DriverSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = DriverSearchForm(data={"username": "TestDriver"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form = DriverSearchForm()
        self.assertFalse(form.is_valid())


class ManufacturerSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = ManufacturerSearchForm(data={"name": "Opel"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self):
        form = ManufacturerSearchForm()
        self.assertFalse(form.is_valid())
