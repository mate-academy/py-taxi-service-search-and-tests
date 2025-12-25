from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            password="pass123"
        )
        self.assertEqual(str(driver), "driver1")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "X5")
