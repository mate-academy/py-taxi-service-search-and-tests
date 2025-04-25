from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer


User = get_user_model()


class CarFormTest(TestCase):
    def setUp(self):
        self.driver1 = User.objects.create_user(
            username="driver1", password="test12345", license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_car_form_valid(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_valid_license_number(self):
        form_data = {
            "username": "newdriver",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number_length(self):
        form_data = {
            "username": "newdriver",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "license_number": "AB123",  # too short
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.driver = User.objects.create_user(
            username="driver1", password="pass123", license_number="ABC12345"
        )

    def test_valid_update_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ54321"})
        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "xyz54321"})  # lowercase
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchFormsTest(TestCase):
    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "john"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "john")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Tesla"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Tesla")

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "BMW")
