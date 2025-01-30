from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tata Motors",
            country="India"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="panjaby",
            password="lkj456_&^%",
            first_name="Radj",
            last_name="Mallah",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tata Motors",
            country="India"
        )
        car = Car.objects.create(
            model="Novus",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
