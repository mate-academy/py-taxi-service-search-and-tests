from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        driver = get_user_model().objects.create(
            username="driver",
            password="bog1234",
            first_name="Bohdan",
            last_name="Bielyi",
            license_number="BBB11111",
        )
        car = Car.objects.create(
            model="HR-V",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)

        self.assertEqual(
            str(car),
            f"{car.model}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="driver",
            password="bog1234",
            first_name="Bohdan",
            last_name="Bielyi",
            license_number="BBB11111",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
