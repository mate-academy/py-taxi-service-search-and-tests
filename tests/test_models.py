from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.driver = Driver.objects.create_user(
            username="test",
            password="PASSWORD",
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_driver_str_method(self):
        self.assertEqual(str(
            self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str_method(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_manufacturer_str_method(self):
        self.assertEqual(str(
            self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )
