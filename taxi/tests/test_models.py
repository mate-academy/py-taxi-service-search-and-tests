from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class ModelTest(TestCase):

    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self) -> None:
        self.assertEqual(
            str(self.car),
            self.car.model
        )

    def test_driver_str(self) -> None:
        full_name = f"({self.driver.first_name} {self.driver.last_name})"
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} {full_name}"
        )

    def test_driver_get_absolute_url(self) -> None:
        self.assertEqual(
            self.driver.get_absolute_url(),
            "/drivers/1/"
        )
