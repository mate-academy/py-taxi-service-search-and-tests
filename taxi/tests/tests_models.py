from django.contrib.auth import get_user, get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelStrTests(TestCase):
    manufacturer = Manufacturer(
        name="<NAME>",
        country="US",
    )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "<NAME> US")

    def test_car_str(self):
        car = Car(
            model="model",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), "model")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="driver",
            first_name="Driver",
            last_name="Driver",
            password="<PASSWORD>",
            license_number="123456",
        )
        self.assertEqual(str(driver), "driver (Driver Driver)")
