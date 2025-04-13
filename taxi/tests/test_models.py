from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTestCase(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="US"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="driver",
            password="Password123",
            first_name="Driver",
            last_name="SurDriver",
        )
        self.assertEqual(
            str(driver),
            "driver (Driver SurDriver)"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="US"
        )
        driver = get_user_model().objects.create(
            username="driver",
            password="Password123",
            first_name="Driver",
            last_name="SurDriver",
        )
        car = Car.objects.create(manufacturer=manufacturer, model="A2")
        car.drivers.add(driver)
        car.save()
        self.assertEqual(str(car), car.model)
