from django.test import TestCase
from taxi.forms import DriverSearchForm, CarSearchForm


class FormsTest(TestCase):
    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "test"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form = CarSearchForm(data={"model": "testmodel"})
        self.assertTrue(form.is_valid())
