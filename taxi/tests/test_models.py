from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        expected_result = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_result)

    def test_create_driver_and_str(self):
        username = "TestUsername"
        password = "Test123#"
        license_number = "TestLicenseNumber"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

        expected_result = (
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEqual(str(driver), expected_result)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="Country"
        )
        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )

        expected_result = car.model
        self.assertEqual(str(car), expected_result)
