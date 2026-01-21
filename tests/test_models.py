from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )

    def test_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} "
            f"{self.manufacturer.country}"
        )


class DriverModelTests(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            "username": "Test Username",
            "first_name": "First",
            "last_name": "Last",
            "password": "test_password123",
            "license_number": "ABC12345"

        }
        self.driver = get_user_model().objects.create_user(
            **self.user_data
        )

    def test_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_create_driver_with_license_number_and_password(self) -> None:
        self.assertEqual(
            self.driver.license_number,
            self.user_data["license_number"]
        )
        self.assertTrue(
            self.driver.check_password(
                self.user_data["password"])
        )

    def test_url(self) -> None:
        self.assertEqual(
            self.driver.get_absolute_url(),
            "/drivers/1/"
        )


class CarModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer
        )

    def test_str(self) -> None:
        self.assertEqual(
            str(self.car),
            f"{self.car.model}"
        )
