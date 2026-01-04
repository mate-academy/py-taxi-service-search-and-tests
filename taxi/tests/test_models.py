from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_license_number(self):
        username = "test"
        password = "1234"
        license_number = "TTT12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test username",
            password="QQww12345",
            first_name="first_test",
            last_name="last_test",
            license_number="TTT12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
