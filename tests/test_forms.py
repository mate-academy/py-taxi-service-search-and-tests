from django.test import TestCase
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class SearchFormTests(TestCase):
    def test_driver_form_valid_data(self):
        form = DriverSearchForm(data={"username": "Sofi"})
        self.assertTrue(form.is_valid())

    def test_driver_form_no_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_car_form_valid_data(self):
        form = CarSearchForm(data={"model": "Mustang"})
        self.assertTrue(form.is_valid())

    def test_car_form_no_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_manufacture_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Lada"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_form_no_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
