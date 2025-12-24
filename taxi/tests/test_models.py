from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacture_str(self):
        manufacture = Manufacturer.objects.create(name="test", country="test1")
        self.assertEqual(
            str(manufacture),
            f"{manufacture.name} {manufacture.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacture = Manufacturer.objects.create(name="test", country="test1")
        car = Car.objects.create(
            model="test",
            manufacturer=manufacture,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
