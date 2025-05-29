# flake8: noqa
from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class TestStrModels(TestCase):

    def test_manufacturer_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_car_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), f"{car.model}({car.manufacturer.name})")

    def test_driver_str_method(self):
        driver = Driver.objects.create(
            username="test_username",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")
