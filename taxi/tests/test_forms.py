from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    CarForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer, Driver


class FormsTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(data={
            "username": "new_driver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertTrue(form.is_valid())

    def test_car_form_valid(self):
        form = CarForm(data={
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
        })
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "XYZ67890"
        })
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={
            "username": "search_driver"
        })
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form = CarSearchForm(data={
            "model": "Corolla"
        })
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data={
            "name": "Tesla"
        })
        self.assertTrue(form.is_valid())
