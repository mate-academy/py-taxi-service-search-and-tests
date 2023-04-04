from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="German"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Johnie",
            password="RE0v4Q4n",
            first_name="John",
            last_name="Smith"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Porsche",
            country="German"
        )
        car = Car.objects.create(
            model="Porsche 911",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
