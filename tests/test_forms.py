from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)


class FormTest(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form_date = {
            "username": "Anatoli123",
            "first_name": "Anatoli",
            "last_name": "Last",
            "password1": "User123.",
            "password2": "User123.",
            "license_number": "REX89345",
        }
        form = DriverCreationForm(data=form_date)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_date)

    def test_driver_licence_update(self):
        form_data = {
            "license_number": "TES99999",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())


class SearchFormsTest(TestCase):
    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "Anatoli"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form = CarSearchForm(data={"model": "Yaris"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_empty(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "Audi"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_empty(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
