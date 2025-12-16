from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    """Test models"""

    def test_manufacturer_str(self):
        """Test manufacturer string representation"""
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        """Test driver string representation"""
        driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        """Test car string representation"""
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        car = Car.objects.create(
            model="Model S",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        """Test creating driver with license number"""
        username = "testdriver"
        license_number = "ABC12345"
        password = "test12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
