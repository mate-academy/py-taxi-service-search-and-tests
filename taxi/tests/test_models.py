from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_string(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_string(self):
        driver = get_user_model().objects.create(
            username="test_username",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_string(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test123"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
