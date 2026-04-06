from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")


class DriverTest(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test Driver",
            password="test123",
            first_name="Test1",
            last_name="Test2",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_create_driver_with_license_number(self):
        license_number = "TES12345"
        username = "Test Driver"
        password = "test123"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))


class CarTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        car = Car.objects.create(
            model="Test Car",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), f"{car.model}")
