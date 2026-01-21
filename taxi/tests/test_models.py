from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverTest(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            first_name="Test First",
            last_name="Test Last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )


class CarTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        car = Car.objects.create(
            model="text",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)
