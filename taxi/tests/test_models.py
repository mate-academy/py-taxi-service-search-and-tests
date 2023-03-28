from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japanese"
        )
        car = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japanese"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver .last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test_password"
        license_number = "AAA12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
