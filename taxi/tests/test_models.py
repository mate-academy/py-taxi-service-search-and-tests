from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test2")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC12345",
        )
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.license_number, "LIC12345")
        self.assertTrue(driver.check_password("test123"))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test2")

        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
