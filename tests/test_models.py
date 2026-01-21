from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_driver",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_driver_car_with_license_number(self):
        username = "test_username"
        password = "test1488"
        license_number = "12345678"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(username, driver.username)
        self.assertEqual(license_number, driver.license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )

        car = Car.objects.create(
            manufacturer=manufacturer,
            model="Test Model"
        )

        self.assertEqual(str(car), f"{car.model}")
