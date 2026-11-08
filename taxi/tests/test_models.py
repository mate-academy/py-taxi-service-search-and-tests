from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Audi", country="Germany")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test1",
            password="test12test",
            first_name="test1",
            last_name="test1",
            license_number="ABC12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Audi", country="Germany")
        car = Car.objects.create(
            model="A6",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
