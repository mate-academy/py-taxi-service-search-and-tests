from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTest(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username, password, license_number = "test", "test123", "HGM15159"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}"
        )
