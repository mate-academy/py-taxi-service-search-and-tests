from django.test import TestCase
from taxi.forms import DriverSearchField, CarSearchField, ManufacturerSearchField


class FormTest(TestCase):
    def test_driver_search_form_valid(self):
        form = DriverSearchField(data={"username": "test_user"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form = CarSearchField(data={"model": "Model S"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchField(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty(self):
        form = DriverSearchField(data={})
        self.assertTrue(form.is_valid())  # Empty search form should still be valid
