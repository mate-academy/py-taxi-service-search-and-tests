from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            manufacturer=Manufacturer.objects.get(name="Toyota"),
            model="Corolla",
        )
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testuser12345",
            license_number="ABC12345",
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )
