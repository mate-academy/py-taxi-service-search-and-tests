from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="test123",
            first_name="user_first_name",
            last_name="user_last_name",
            license_number="ABC12345",
        )

        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_name",
            country="test_country"
        )

        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )
