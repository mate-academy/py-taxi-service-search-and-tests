from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )

    def test_manufacturer_format_str(self):
        self.assertEqual(
            str(self.manufacturer), f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="PASSword123&%",
            first_name="Test First Name",
            last_name="Test Last Name",
            email="test12@testmail.com",
            license_number="AAA12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_car_str(self):
        car = Car.objects.create(model="Test Model", manufacturer=self.manufacturer)
        self.assertEqual(
            str(car),
            car.model,
        )

    def test_driver_with_license_number(self):
        username = "test_driver"
        password = "PASSword123&%"
        license_number = "AAA12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
