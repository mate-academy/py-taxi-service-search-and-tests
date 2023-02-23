from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverLicenseUpdateForm,
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.driver1 = get_user_model().objects.create(username="testuser1", license_number=1)
        self.driver2 = get_user_model().objects.create(username="testuser2", license_number=2)

    def test_car_form_valid(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver1, self.driver2],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestDriverCreationForm(TestCase):
    def test_form_valid_data(self):
        form = DriverCreationForm(data={
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ABC12345",
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_license_number(self):
        form = DriverCreationForm(data={
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "123456789",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class TestDriverLicenseUpdateForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="Test",
            last_name="User",
            license_number="ABC12345",
        )

    def test_form_valid_data(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "XYZ98765"},
            instance=self.user
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.license_number, "XYZ98765")

    def test_form_invalid_license_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "123456789"},
            instance=self.user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class TestDriverSearchForm(TestCase):
    def test_form_valid(self):
        form_data = {"user_name": "john"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestCarSearchForm(TestCase):
    def test_form_valid(self):
        form_data = {"model": "Camry"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestManufacturerSearchForm(TestCase):
    def test_form_valid(self):
        form_data = {"model": "Camry"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
