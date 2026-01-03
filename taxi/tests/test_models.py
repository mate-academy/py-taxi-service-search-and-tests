from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="username",
            email="email@test.test",
            first_name="firstname",
            last_name="lastname",
            password="test123",
            license_number="ABC123"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        car = Car.objects.create(
            manufacturer=manufacturer,
            model="test_model",
        )
        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license(self):
        username = "username"
        first_name = "first_name"
        last_name = "last_name"
        password = "test123"
        license_number = "ABC123"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, "username")
        self.assertEqual(driver.first_name, "first_name")
        self.assertEqual(driver.last_name, "last_name")
        self.assertEqual(driver.license_number, "ABC123")
        self.assertTrue(driver.check_password(password))
