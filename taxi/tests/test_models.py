from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_create_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            license_number="TES12345",
            password="test_password"
        )
        self.assertEqual(driver.username, "test_username")
        self.assertEqual(driver.license_number, "TES12345")
        self.assertTrue(driver.check_password("test_password"))
