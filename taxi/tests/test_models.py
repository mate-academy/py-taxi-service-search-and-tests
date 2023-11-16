from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="BYD", country="China")
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        password = "Test123"
        driver = get_user_model().objects.create_user(
            username="test",
            password=password,
            first_name="test_first",
            last_name="test_second",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertTrue(driver.check_password(password))

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "Test123"
        license_number = "DWA12345"
        driver = get_user_model().objects.create(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
