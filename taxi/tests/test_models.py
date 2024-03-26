from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test",
            first_name="test",
            last_name="test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test",
            first_name="test",
            last_name="test",
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test",
            first_name="test",
            last_name="test",
        )
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test"
        )
        car = Car.objects.create(
            model="Test Car",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), f"{car.model}")
