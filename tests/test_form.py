from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
    DriverSearchForm,
    CarSearchForm)
from taxi.models import Car, Driver, Manufacturer


class TestCarForm(TestCase):
    def test_valid_form(self):
        data = {
            "model": "Test Car",
            "manufacturer": Manufacturer.objects.create(
                name="Test Manufacturer",
                country="Test Country"
            ),
            "drivers": [Driver.objects.create_user(
                username="testuser",
                email="test@example.com",
                password="test123",
                license_number="123456")]
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "model": "",
            "manufacturer": "",
            "drivers": []
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())


class TestDriverCreationForm(TestCase):
    def test_valid_form(self):
        data = {
            "username": "test_user",
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "ZXC12312",
            "first_name": "Test",
            "last_name": "User"
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
            "license_number": "",
            "first_name": "",
            "last_name": ""
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())


class TestDriverLicenseUpdateForm(TestCase):
    def test_valid_form(self):
        driver = Driver.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="test123",
            license_number="QWE12312"
        )
        data = {
            "license_number": "ZXC12312"
        }
        form = DriverLicenseUpdateForm(data=data, instance=driver)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        driver = Driver.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="test123",
            license_number="QWE12312"
        )
        data = {
            "license_number": ""
        }
        form = DriverLicenseUpdateForm(data=data, instance=driver)
        self.assertFalse(form.is_valid())


class TestManufacturerSearchForm(TestCase):
    def test_valid_form(self):
        data = {
            "name": "Test Manufacturer"
        }
        form = ManufacturerSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "name": ""
        }
        form = ManufacturerSearchForm(data=data)
        self.assertTrue(form.is_valid())


class TestDriverSearchForm(TestCase):
    def test_valid_form(self):
        data = {
            "username": "testuser"
        }
        form = DriverSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "username": ""
        }
        form = DriverSearchForm(data=data)
        self.assertTrue(form.is_valid())


class TestCarSearchForm(TestCase):
    def test_valid_form(self):
        data = {
            "model": "Test Car"
        }
        form = CarSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "model": ""
        }
        form = CarSearchForm(data=data)
        self.assertTrue(form.is_valid())
