from django.test import TestCase

from taxi.models import (
    Manufacturer,
    Driver,
    Car
)


class ManufacturerModelTestCase(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, "Tesla")
        self.assertEqual(self.manufacturer.country, "USA")

    def test_str_method(self):
        self.assertEqual(str(self.manufacturer), "Tesla USA")


class CarModelTestCase(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.car = Car.objects.create(
            model="Model S", manufacturer=self.manufacturer
        )

    def test_car_creation(self):
        self.assertEqual(self.car.model, "Model S")
        self.assertEqual(self.car.manufacturer.name, "Tesla")

    def test_str_method(self):
        self.assertEqual(str(self.car), "Model S")


class DriverModelTestCase(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.driver = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="ABC123",
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.username, "john_doe")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.license_number, "ABC123")

    def test_str_method(self):
        self.assertEqual(str(self.driver), "john_doe (John Doe)")
