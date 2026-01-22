from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="United States"
        )

        self.assertEqual(str(manufacturer), "Audi United States")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Max",
            password="12345678",
            first_name="Max",
            last_name="Muha",
        )
        self.assertEqual(str(driver), "Max (Max Muha)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="United States"
        )
        car = Car.objects.create(
            model="RS6 Avant",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "RS6 Avant")
