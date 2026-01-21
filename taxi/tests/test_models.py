from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany"
        )
        self.driver = get_user_model().objects.create(
            username="user",
            password="userpass123",
            first_name="Michael",
            last_name="Schumacher",
            license_number="ABC12345"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Volkswagen Germany")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "user (Michael Schumacher)")

    def test_car_str(self):
        car = Car.objects.create(
            model="Touareg",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), "Touareg")

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.license_number, "ABC12345")
