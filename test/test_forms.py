from django.test import TestCase
from django.core.exceptions import ValidationError
from taxi.models import Manufacturer, Driver, Car
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarsModelSearchForm,
    ManufacturersNameSearchForm,
    DriversUsernameSearchForm,
    validate_license_number
)


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = (
            Manufacturer.objects.create(
                name="Tesla",
                country="USA"))
        self.driver = (
            Driver.objects.create(
                username="test_driver",
                license_number="ABC12345",
                first_name="John",
                last_name="Doe"))

    def test_form_is_valid(self):
        data = {
            "model": "Model S",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_form_is_valid(self):
        data = {
            "username": "test.user",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "strong_P@ssword123",
            "password2": "strong_P@ssword123",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_license_number_validation_error(self):
        data = {"username": "user", "license_number": "wrong_format"}
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_update_is_valid(self):
        data = {"license_number": "XYZ98765"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())


class LicenseNumberValidatorTest(TestCase):
    def test_validate_license_number_success(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_validate_license_number_fails(self):
        with self.assertRaises(ValidationError):
            validate_license_number("123ABCDE")
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")


class SearchFormsTest(TestCase):
    def test_car_model_search_is_valid(self):
        form = CarsModelSearchForm(data={"model": "Tesla"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_is_valid(self):
        form = ManufacturersNameSearchForm(data={"name": "Ford"})
        self.assertTrue(form.is_valid())

    def test_username_search_is_valid(self):
        form = DriversUsernameSearchForm(data={"username": "admin.user"})
        self.assertTrue(form.is_valid())
