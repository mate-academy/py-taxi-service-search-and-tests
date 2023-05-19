from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test country"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
        )
        url = driver.get_absolute_url()
        expected_url = f"/drivers/{driver.id}/"

        self.assertIsNotNone(url)
        self.assertEqual(url, expected_url)

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test country"
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), f"{car.model}")
