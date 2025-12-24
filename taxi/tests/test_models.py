from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Car, Manufacturer, Driver


class ModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "Test Model")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test Username",
            first_name="Test First Name",
            last_name="Test Last Name"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "Test Username"
        password = "test123"
        license_number = "AAA11111"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            country="Test Country",
            name="Test Name"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}")
