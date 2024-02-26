from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.license_number = "BOB11111"
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            license_number=self.license_number,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="TestCountry"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_license_number(self):
        self.assertEqual(self.driver.license_number, self.license_number)

    def test_car_str(self):
        car = Car.objects.create(
            model="Test Ferrari",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )
