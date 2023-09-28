from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="P@ssword23",
            first_name="Ryan",
            last_name="Gosling",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="Ukraine"
        )
        self.car = Car.objects.create(
            model="test_car", manufacturer=self.manufacturer
        )

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.user),
            f"{self.user.username} "
            f"({self.user.first_name} {self.user.last_name})",
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), self.car.model)
