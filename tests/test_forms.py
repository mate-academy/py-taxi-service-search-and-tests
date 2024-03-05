from django.test import TestCase
from taxi.forms import (CarForm,
                        CarSearchForm,
                        DriverCreationForm,
                        DriverLicenseUpdateForm,
                        DriverSearchForm,
                        ManufacturerSearchForm)
from taxi.models import Car, Driver, Manufacturer


class CarFormTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.driver = Driver.objects.create(
            username="test_driver_1",
            password="pass1234", license_number="TES12345")

    def test_car_form_valid(self) -> None:
        form = CarForm(
            data={"model": "Test Model",
                  "manufacturer": self.manufacturer.id,
                  "drivers": [self.driver.id]}
        )
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form_valid(self):
        form = CarSearchForm(data={"model": "Test Model"})
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(
            data={
                "username": "test_driver_1",
                "password1": "test12345",
                "password2": "test12345",
                "license_number": "TES12345",
                "first_name": "First",
                "last_name": "Last"})
        valid = form.is_valid()
        if not valid:
            print(form.errors)
        self.assertTrue(valid)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TES12345"})
        self.assertTrue(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "test_driver_1"})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "Test Manufacturer"})
        self.assertTrue(form.is_valid())
