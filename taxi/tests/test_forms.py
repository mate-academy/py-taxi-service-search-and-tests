from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriversSearchForm,
    CarsSearchForm,
    ManufacturersSearchForm

)

from taxi.models import Manufacturer, Driver


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )

        self.driver = Driver.objects.create_user(
            username="user1",
            password="password",
            license_number="ABC12345"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "model2",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }

        form = CarForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }

        form = CarForm(data=form_data)

        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):

        form_data = {
            "username": "test_driver",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "ABC12345",
            "first_name": "test",
            "last_name": "driver",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        form_data = {
            "username": "",
            "password1": "password1",
            "password2": "password1",
            "license_number": "ABC12345",
            "first_name": "",
            "last_name": "",
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "ABC12345"
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {
            "license_number": "acb1234t"
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestDriversSearchForm(TestCase):
    def test_drivers_search_form_valid(self):
        form_data = {
            "username": "username"
        }

        form = DriversSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestCarSearchForm(TestCase):
    def test_drivers_search_form_valid(self):
        form_data = {
            "model": "model"
        }

        form = CarsSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestManufacturerSearchForm(TestCase):
    def test_manufacturers_search_form_valid(self):
        form_data = {
            "name": "name"
        }

        form = ManufacturersSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
