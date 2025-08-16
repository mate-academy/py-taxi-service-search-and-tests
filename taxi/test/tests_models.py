from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test1")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_second",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_license(self):
        driver = get_user_model().objects.create_user(
            username="test", password="test123", license_number="ABC12345"
        )
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertTrue(driver.check_password("test123"))
