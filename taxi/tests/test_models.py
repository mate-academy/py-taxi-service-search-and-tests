from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class CarModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.driver = get_user_model().objects.create_user(
            username="Test User",
            password="Test Password",
            license_number="ABC12345",
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)

        self.assertEqual(str(car), car.model)


class DriverModelTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test User",
            password="Test Password",
            license_number="ABC12345",
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")