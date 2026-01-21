from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create()
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        car = Car.objects.create()
        self.assertEqual(
            str(car),
            car.model
        )

    def test_driver_str(self):
        driver = Driver.objects.create()
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
