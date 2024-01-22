from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country",
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), f"{car.model}")
