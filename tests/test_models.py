from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_Manufacturer",
            country="Test_Country"
        )
        self.assertEqual(
            f"{manufacturer.name} {manufacturer.country}",
            str(manufacturer)
        )

    def test_driver_str(self):
        username = "Driver"
        password = "driver456"
        license_number = "MOP23456"
        first_name = "test_first"
        last_name = "test_last"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_Manufacturer",
            country="Test_Country"
        )
        car = Car.objects.create(model="Test_Car", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
