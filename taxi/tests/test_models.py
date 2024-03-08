from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Zaz",
            country="Ukraine"
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Zaz",
            country="Ukraine"
        )
        driver = get_user_model().objects.create(
            username="username",
            password="password"
        )
        car = Car.objects.create(
            model="Forza",
            manufacturer=manufacturer
        )
        car.drivers.set((driver, ))
        self.assertEqual(str(car), f"{car.model}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="username",
            password="password",
            first_name="first_name",
            last_name="last_name"
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_create_driver_with_license_plate(self):
        username = "username"
        password = "password"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
