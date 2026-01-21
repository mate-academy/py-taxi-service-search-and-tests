from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Car, Manufacturer
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
    validate_license_number
)


class CarFormTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk]
        }

    def test_car_form_valid(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form = CarForm(data={})
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "Driver"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form = DriverCreationForm(data={})
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "XYZ67890"
        }
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {
            "license_number": "XYZ"
        }
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertFalse(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_driver_search_form(self):
        form_data = {"username": "driver1"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form(self):
        form_data = {"model": "Corolla"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form(self):
        form_data = {"model": "Toyota"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ValidateLicenseNumberTest(TestCase):
    def test_validate_license_number_valid(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_validate_license_number_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_validate_license_number_invalid_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_validate_license_number_invalid_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12A45")
