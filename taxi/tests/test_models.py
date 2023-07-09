from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="driver",
            first_name="John",
            last_name="Doe",
            password="driver12345",
            license_number="ABC12345"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Camry")

    def test_create_driver_with_license_number(self):
        username = "driver"
        password = "driver12345"
        license_number = "ABC12345"

        self.assertEqual(self.driver.username, username)
        self.assertTrue(self.driver.check_password(password))
        self.assertEqual(self.driver.license_number, license_number)

    def test_driver_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")
