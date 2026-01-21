from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer
from taxi.forms import (
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverCreationForm)


class FormTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test",
            "password1": "Str0ngP@ssw0rd!",
            "password2": "Str0ngP@ssw0rd!",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "UNI12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def driver_license_update_form(self):
        form_data = {
            "license_number": "NEW12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_invalid(self):
        form_data = {
            "license_number": "NEW"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class TestSearchForms(TestCase):
    def setUp(self):
        self.drivers = [
            get_user_model().objects.create_user(
                username=f"driver{i}",
                password="testpass123",
                first_name=f"Test{i}",
                last_name="Driver",
                license_number=f"UNI{i : 05}"
            ) for i in range(5)
        ]

        self.manufacturers = [
            Manufacturer.objects.create(
                name=f"Manufacturer {i}",
                country="Test Country"
            ) for i in range(5)
        ]

        self.cars = [
            Car.objects.create(
                model=f"Model {i}",
                manufacturer=self.manufacturers[i % 5]
            ) for i in range(10)
        ]

    def test_driver_search_form(self):
        form_data = {"username": "driver1"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        drivers = get_user_model().objects.filter(
            username__icontains=form_data["username"]
        )
        self.assertEqual(set(drivers), {self.drivers[1]})

        for driver in self.drivers:
            if driver != self.drivers[1]:
                self.assertNotIn(driver, drivers)

    def test_car_search_form(self):
        form_data = {"model": "Model 2"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        cars = Car.objects.filter(model__icontains=form_data["model"])
        self.assertEqual(set(cars), {self.cars[2]})

        for car in self.cars:
            if car != self.cars[2]:
                self.assertNotIn(car, cars)

    def test_manufacturer_search_form(self):
        form_data = {"name": "Manufacturer 3"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        manufacturers = Manufacturer.objects.filter(
            name__icontains=form_data["name"]
        )
        self.assertEqual(set(manufacturers), {self.manufacturers[3]})

        for manufacturer in self.manufacturers:
            if manufacturer != self.manufacturers[3]:
                self.assertNotIn(manufacturer, manufacturers)
