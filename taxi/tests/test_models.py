from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTests(TestCase):
    def test_str_returns_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        manufacturer = str(manufacturer)

        self.assertEqual(manufacturer, "BMW Germany")


class DriverModelTests(TestCase):
    def test_str_return_driver(self):
        driver = Driver.objects.create(
            username="jim.hopper",
            first_name="Jim",
            last_name="Hopper",
            license_number="AB1234CD",
        )

        driver = str(driver)
        self.assertEqual(driver, "jim.hopper (Jim Hopper)")

    def test_get_absolute_url_driver(self):
        driver = Driver.objects.create(
            id=10,
            license_number="AB1234CD"
        )

        actual = driver.get_absolute_url()

        self.assertEqual(actual, "/drivers/10/")


class CarModelTests(TestCase):
    def test_str_returns_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        car = Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )

        actual = str(car)

        self.assertEqual(actual, "BMW")
