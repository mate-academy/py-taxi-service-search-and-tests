from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.driver = get_user_model().objects.create_user(
            username="bob123",
            password="test123",
            first_name="Bob",
            last_name="James",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="A6",
            manufacturer=self.manufacturer,
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
