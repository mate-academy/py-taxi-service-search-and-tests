from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford Motor Company",
            country="USA"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford Motor Company",
            country="USA"
        )
        car = Car.objects.create(
            model="Toyota Yaris",
            manufacturer=manufacturer
        )

        self.assertEqual(
            str(car),
            f"{car.model}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Anton123",
            password="anton12345",
            first_name="Anton",
            last_name="Sanchos"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "Anton123"
        password = "anton12345"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
