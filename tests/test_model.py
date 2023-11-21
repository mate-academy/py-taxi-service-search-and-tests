from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="ivanovich",
            password="test12345",
            first_name="Ivan",
            last_name="Ivanov"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        car = Car.objects.create(
            model="Grand Cherokee",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
