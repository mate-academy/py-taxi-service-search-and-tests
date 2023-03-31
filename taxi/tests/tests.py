from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        username = "test"
        first_name = "test"
        last_name = "test"
        driver = get_user_model().objects.create_user(
            username=username,
            password="test123456",
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(str(driver), f"{username} ({first_name} {last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )

        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
