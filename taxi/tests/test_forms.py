from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm
)
from taxi.models import Car, Driver, Manufacturer


class TestForms(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="test_model"
        )
        self.driver = Driver.objects.create(
            username="test_driver",
            license_number="test_license_number"
        )

    def test_car_form_valid_data(self):
        form_data = {
            "manufacturer": self.manufacturer,
            "model": "test_model",
            "drivers": [self.user.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_valid_data(self):
        form_data = {
            "username": "new_user",
            "password1": "ds3fk2df1223",
            "password2": "ds3fk2df1223",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "Driver"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_valid_data(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_validate_license_number(self):
        self.assertRaises(
            ValidationError,
            validate_license_number,
            "ABC1234"
        )
        self.assertRaises(
            ValidationError,
            validate_license_number,
            "abc12345"
        )
        self.assertRaises(
            ValidationError,
            validate_license_number,
            "ABC1XY45"
        )

    def test_driver_username_search_form_valid_data(self):
        form_data = {"username": "test_user"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_model_search_form_valid_data(self):
        form_data = {"model": "test_model"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_name_search_form_valid_data(self):
        form_data = {"name": "test_manufacturer"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
