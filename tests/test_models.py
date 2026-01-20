from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="DM",
            country="USA"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Anatoli123",
            password="User123.",
            first_name="Anatoli",
            last_name="Last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="GM",
            country="USA"
        )
        car = Car.objects.create(
            model="Buick",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            car.model
        )
