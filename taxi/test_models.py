from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="qwerty",
            country="qwerty"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}"
        )

    def test_create_driver_without_license_number(self):
        user = Driver.objects.create_user(
            username="qwerty",
            password="qwerty",
            first_name="qwerty",
            last_name="qwerty",
        )
        self.assertIsNotNone(user)

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="qwerty",
            password="qwerty",
            first_name="qwerty",
            last_name="qwerty",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "f"({driver.first_name} "f"{driver.last_name})"
        )

    def test_delete_driver(self):
        driver = Driver.objects.create_user(
            username="qwerty",
            password="qwerty",
            first_name="qwerty",
            last_name="qwerty",
        )
        driver.delete()
        self.assertIsNone(Driver.objects.filter(username="qwerty").first())

    def test_add_driver_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="qwerty",
            country="qwerty"
        )
        car = Car.objects.create(
            model="qwerty",
            manufacturer=manufacturer
        )
        driver = Driver.objects.create_user(
            username="qwerty",
            password="qwerty",
            first_name="qwerty",
            last_name="qwerty",
        )
        car.drivers.add(driver)
        self.assertIn(driver, car.drivers.all())
