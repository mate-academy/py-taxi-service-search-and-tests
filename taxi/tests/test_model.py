from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="TestCountry"
        )
        self.assertEqual(
            str(manufacturer),
            manufacturer.name + " " + manufacturer.country
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="TestCountry"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEqual(
            str(car),
            car.model
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
