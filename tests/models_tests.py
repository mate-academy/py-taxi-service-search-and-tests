from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Czech Republic"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverTests(TestCase):
    def test_driver_str(self):
        driver = Driver.objects.create(
            username="bobby",
            first_name="Bobby",
            last_name="Fisher"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )


class CarTests(TestCase):
    def test_car_str(self):
        car = Car.objects.create(
            model="Lexus",
            manufacturer=Manufacturer.objects.create(name="Mazda"),
        )
        self.assertEqual(str(car), car.model)
