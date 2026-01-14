from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import (
    CarForm, DriverCreationForm, DriverLicenseUpdateForm,
    DriverUsernameSearchForm, CarModelSearchForm, ManufacturerNameSearchForm
)
from taxi.models import Car, Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="ABC12345"
        )

    def test_valid_car_form(self):
        form_data = {"model": "Corolla", "manufacturer": self.manufacturer.pk, "drivers": [self.driver.pk]}
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_car_form(self):
        form = CarForm(data={})  # пустая форма
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_valid_driver_creation_form(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "XYZ67890",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "1234",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_invalid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "1234"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchFormsTest(TestCase):
    def test_driver_username_search_form(self):
        form = DriverUsernameSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())

    def test_car_model_search_form(self):
        form = CarModelSearchForm(data={"model": "Tesla"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_name_search_form(self):
        form = ManufacturerNameSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
