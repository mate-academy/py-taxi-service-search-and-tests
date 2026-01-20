from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriversSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer, Car
from django.contrib.auth import get_user_model


class FormTests(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_form_valid_data(self):
        form = CarForm(
            data={
                "model": "Camry",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk]
            }
        )
        self.assertTrue(form.is_valid())

    def test_car_form_no_data(self):
        form = CarForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_driver_creation_form_valid_data(self):
        form = DriverCreationForm(data={
            "username": "driver2",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "DEF67890",
            "first_name": "Jane",
            "last_name": "Doe"
        })
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form = DriverCreationForm(data={
            "username": "driver3",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "A1C67890",
            "first_name": "Mark",
            "last_name": "Smith"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_valid_data(self):
        form = DriverLicenseUpdateForm(
            data={
                "license_number": "XYZ67890"
            },
            instance=self.driver
        )
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_license(self):
        form = DriverLicenseUpdateForm(
            data={
                "license_number": "A1C67890"
            },
            instance=self.driver
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_drivers_search_form(self):
        form = DriversSearchForm(data={"first_name": "John"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["first_name"], "John")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Corolla"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Corolla")

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")
