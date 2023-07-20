from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.models import Car, Manufacturer


class ModelsTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="LaLaLand"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "test")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="LaLaLand"
        )
        self.assertEqual(str(manufacturer), "TestName LaLaLand")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            password="testpasswd",
            first_name="Rick",
            last_name="Astley"
        )
        self.assertEqual(str(driver), f"{driver.username} ("
                                      f"{driver.first_name} "
                                      f"{driver.last_name})")

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
