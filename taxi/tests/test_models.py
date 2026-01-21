from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class CarTests(TestCase):
    def test_car_str(self):
        car = Car.objects.create(model="test")
        self.assertEqual(str(car), car.model)


class DriverTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            license_number="ABC123456",
            username="test-name",
            password="test123456",
            first_name="test-first",
            last_name="test-last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )


class ManufacturerTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test-name",
            country="test-country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )
