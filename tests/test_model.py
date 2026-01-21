from unittest import TestCase

from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test ", country="test "
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_second",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
