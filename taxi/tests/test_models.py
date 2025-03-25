from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country",
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name}"
                         f" {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            license_number="TES12345",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name}"
                         f" {driver.last_name})")

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "Test Pseudonym"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.check_password(password), True)
