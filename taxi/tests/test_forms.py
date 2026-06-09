from django.test import TestCase

from taxi.forms import (
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Driver, Manufacturer


class SearchFormTests(TestCase):
    def test_driver_username_search_form_valid(self):
        data = {"username": "test_user"}
        form = DriverUsernameSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_car_model_search_form_valid(self):
        data = {"model": "test_model"}
        form = CarModelSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_name_search_form_valid(self):
        data = {"name": "test_manufacturer"}
        form = ManufacturerNameSearchForm(data=data)
        self.assertTrue(form.is_valid())


class CarFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="username",
            password="password1",
            license_number="ADM12345",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="countrytest",
        )

    def test_car_form_with_valid_data(self):
        data = {
            "model": "testmodel",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())

    def test_car_form_raises_error(self):
        data = {
            "model": "testmodel",
            "manufacturer": self.manufacturer.id,
            "drivers": [999]
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)


class DriverFormTests(TestCase):
    def test_driver_create_form_with_valid_data(self):
        data = {
            "username": "test_username",
            "password1": "PASw1%rd",
            "password2": "PASw1%rd",
            "license_number": "ADM12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_driver_license_form_with_invalid_length(self):
        data = {"license_number": "ADM123"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_driver_license_form_with_invalid_letters(self):
        data = {"license_number": "aDM12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_driver_license_form_with_invalid_digits(self):
        data = {"license_number": "ADM1234s"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )
