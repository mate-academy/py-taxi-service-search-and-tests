from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):

    def test_manufacturer_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTests(TestCase):
    def test_driver_str_method(self):
        driver = get_user_model().objects.create_user(
            username="test",
            first_name="Test",
            last_name="TesT",
            password="test1234",
            license_number="QWE12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )


class CarModelTests(TestCase):
    def test_car_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        car = Car.objects.create(
            model="Cybertruck",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
