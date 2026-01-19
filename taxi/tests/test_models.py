from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        """
        Test that manufacturer str representation works correctly
        """
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry",
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        """
        Test that driver str representation works correctly
        """
        driver = get_user_model().objects.create_user(
            username="TestUser",
            password="test123",
            first_name="TestFirstName",
            last_name="TestLastName",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_create_with_license(self):
        """
        Test that driver creation with license works correctly
        """
        username = "TestUser1"
        password = "test123"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        """
        Test that car str representation works correctly
        """
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )

        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )

        self.assertEqual(
            str(car),
            car.model
        )
