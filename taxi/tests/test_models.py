from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test.driver",
            password="test12345",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
