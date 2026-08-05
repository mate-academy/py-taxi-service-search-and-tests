from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test Driver",
            password="test1234",
            first_name="Test First",
            last_name="Test Last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        driver = get_user_model().objects.create_user(
            username="Test Driver",
            password="test1234",
            first_name="Test First",
            last_name="Test Last"
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEqual(str(car), car.model)

    def test_license_number(self):
        username = "Test Driver"
        password = "test1234"
        license_number = "Test License Number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.check_password(password), True)
        self.assertEqual(driver.license_number, license_number)
