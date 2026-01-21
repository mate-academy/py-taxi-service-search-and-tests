from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="USA",
        )
        self.car = Car.objects.create(
            model="VW Tiguan Allspace R-Line Black Edition",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="test_bronislav",
            email="bronislav@example.com",
            password="12345678!sho_ti_smotrish",
            first_name="Bronislav",
            last_name="Veprintsev",
            license_number="IUH54321",
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} "
            f"{self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )
