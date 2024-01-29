from django.test import TestCase
from taxi.forms import DriverCreationForm, CarForm, DriverSearchForm, ManufacturerSearchForm, CarSearchForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_date = {
            "username": "test",
            "password1": "testPASSWORD",
            "password2": "testPASSWORD",
            "license_number": "RDF12312",
            "first_name": "test_first",
            "last_name": "test_last"
        }
        form = DriverCreationForm(data=form_date)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_date)


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_is_valid(self):
        form_date = {"username": "test"}
        form = DriverSearchForm(data=form_date)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_is_valid(self):
        form_date = {"name": "testname"}
        form = ManufacturerSearchForm(data=form_date)
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form_is_valid(self):
        form_date = {"model": "testmodel"}
        form = CarSearchForm(data=form_date)
        self.assertTrue(form.is_valid())
