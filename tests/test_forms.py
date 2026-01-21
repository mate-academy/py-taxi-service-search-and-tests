from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    CarForm,
    ManufacturerSearchForm)
from taxi.models import (
    Driver,
    Car,
    Manufacturer)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "ab123",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number",
                      form.errors)


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan")

        self.driver = Driver.objects.create(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe",
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_car_form_invalid(self):
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid(self):
        form_data = {
            "name": "Toyota",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_manufacturer_search_form_invalid(self):
        form_data = {}
        form = ManufacturerSearchForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=f"Form errors: {form.errors}")
