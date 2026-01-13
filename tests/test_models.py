from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


# Create your tests here.
class ModelTests(TestCase):
    def test_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="Test_country",
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver(self):
        driver = get_user_model().objects.create(
            username="test_username",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_create_driver_with_license_numer(self):
        username = "test_username"
        password = "test123"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
