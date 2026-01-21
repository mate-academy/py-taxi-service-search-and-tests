from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="No country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def test_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="user",
            password="mypass",
            first_name="first",
            last_name="last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )


class CarModelTest(TestCase):
    def test_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="user",
            country="best country"
        )
        car = Car.objects.create(
            model="bbq",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
