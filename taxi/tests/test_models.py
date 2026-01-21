from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_license_number(self):
        license_number = "AAA55555"
        password = "PASSWORD123"
        driver = get_user_model().objects.create_user(
            username="test username",
            password=password,
            email="email@email.com",
            license_number=license_number,
        )
        self.assertEqual(
            driver.license_number,
            license_number,
        )
        self.assertTrue(driver.check_password(password))

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test username",
            password="<PASSWORD>",
            email="email@email.com",
            license_number="AAA55555",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country",
        )
        car = Car.objects.create(
            manufacturer=manufacturer,
            model="test model",
        )
        self.assertEqual(
            str(car),
            car.model
        )
