from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="password123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="ASD12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_car_model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self) -> None:
        username = "test_username"
        license_number = "AAA12345"
        password = "password123"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            password=password,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
