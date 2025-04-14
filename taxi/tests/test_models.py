from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="SuperFastDriver",
            first_name="Tom",
            last_name="Smith"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(model="X3", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "SuperFastDriver"
        license_number = "ABC12345"
        driver = get_user_model().objects.create(
            username=username,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
