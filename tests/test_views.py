from django.test import TestCase, Client

from taxi.forms import DriverSearchForm, ManufacturerSearchForm, CarSearchForm


class TestSearchFunctionDriver(TestCase):
    def test_driver_search_form_is_valid(self):
        form_data = {
            "username": "test user"
        }
        form = DriverSearchForm(data=form_data)
        self.assertEqual(form.is_valid(), True)


class TestSearchFunctionManufacturer(TestCase):
    def test_manufacturer_search_form_is_valid(self):
        form_data = {"name": "test manufacturer"}

        form = ManufacturerSearchForm(data=form_data)

        self.assertEqual(form.is_valid(), True)


class TestSearchFunctionCar(TestCase):
    def test_car_search_form_is_valid(self):
        form_data = {"model": "test car"}
        form = CarSearchForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
