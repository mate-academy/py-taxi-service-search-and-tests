from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country"
        )

        self.assertEqual(str(manufacturer), f"Test Country")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test",
            password="test1234",
            first_name="Test First",
            last_name="Test Last"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country"
        )
        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):
        username = "Test"
        password = "test1234"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
