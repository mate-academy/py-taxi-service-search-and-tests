from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    def test_car_model_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "test")

    def test_manufacturer_model_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_model_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="first_test",
            last_name="last_test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
