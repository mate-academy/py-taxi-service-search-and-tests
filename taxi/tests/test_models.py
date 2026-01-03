from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Test username",
            password="Pass1234",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
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
        car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)
