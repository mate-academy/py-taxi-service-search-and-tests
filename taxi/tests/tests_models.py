from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test.username",
            first_name="test.first_name",
            last_name="test.last_name"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver(self):
        username = "test.username"
        first_name = "test.first_name"
        last_name = "test.last_name"
        password = "TestPassword"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")

        car = Car.objects.create(
            model="Focus",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
