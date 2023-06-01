from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Test"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="password123",
            first_name="Test first",
            last_name="Test last"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_srt(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="Test"
        )
        driver = get_user_model().objects.create_user(
            username="test",
            password="password123",
            first_name="Test first",
            last_name="Test last"
        )
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer,
        )
        drivers = (driver,)
        car.drivers.set(drivers)

        self.assertEqual(str(car), car.model)
