from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        expected_string = (f"{manufacturer.name}"
                           f" {manufacturer.country}")
        self.assertEqual(str(manufacturer), expected_string)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        expected_string = (f"{driver.username}"
                           f" ({driver.first_name}"
                           f" {driver.last_name})")
        self.assertEqual(str(driver), expected_string)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test_username"
        first_name = "test_first_name"
        password = "test_password"
        license_number = "AXC59420"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
