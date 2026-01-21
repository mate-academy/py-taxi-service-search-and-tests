from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            first_name="TestFirst",
            last_name="TestLast",
            password="TestPassword",
            username="TestUsername",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_user(self):
        driver = get_user_model().objects.create_user(
            password="TestPassword",
            username="TestUsername",
            license_number="TestLicense"
        )
        self.assertEqual(driver.license_number, "TestLicense")
        self.assertTrue(driver.check_password("TestPassword"))
