from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer, Driver


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry"
        )

        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="testpassword",
            license_number="ABC12345"
        )

    def test_car_form_valid(self):
        form_data = {
            'model': 'TestCar',
            'manufacturer': self.manufacturer.id,
            'drivers': [self.driver.id],
        }

        form = CarForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            'model': '',
            'manufacturer': self.manufacturer.id,
            'drivers': [self.driver.id],
        }

        form = CarForm(data=form_data)

        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        """
        Test that DriverCreationForm is valid with correct data.
        """
        form_data = {
            'username': 'testdriver',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'license_number': 'ABC12345',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        """
        Test that DriverCreationForm is invalid with incorrect data.
        """
        form_data = {
            'username': '',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'license_number': 'InvalidLicense',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        """
        Test that DriverLicenseUpdateForm is valid with correct data.
        """
        form_data = {
            'license_number': 'ABC12345',
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        """
        Test that DriverLicenseUpdateForm is invalid with incorrect data.
        """
        form_data = {
            'license_number': 'InvalidLicense',
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_valid(self):
        """
        Test that DriverSearchForm is valid with correct data.
        """
        form_data = {
            'username': 'testuser',
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form_valid(self):
        """
        Test that CarSearchForm is valid with correct data.
        """
        form_data = {
            'model': 'TestModel',
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid(self):
        """
        Test that ManufacturerSearchForm is valid with correct data.
        """
        form_data = {
            'name': 'TestManufacturer',
            'country': 'TestCountry',
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
