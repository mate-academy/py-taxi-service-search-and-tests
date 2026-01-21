from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class DriverCreationTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_valid(
            self
    ):
        form_data = {
            "username": "test_user",
            "password1": "test123test",
            "password2": "test123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES44422",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormsTest(TestCase):
    def test_car_with_valid_data(self):
        form = CarSearchForm(data={"model": "Suzuki"})
        self.assertTrue(form.is_valid())

    def test_car_with_invalid_data(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_manufacturer_with_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_with_invalid_data(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_driver_with_valid_data(self):
        form = DriverSearchForm(data={"username": "admin"})
        self.assertTrue(form.is_valid())

    def test_driver_with_invalid_data(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
