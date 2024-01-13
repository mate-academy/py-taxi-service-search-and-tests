from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class TestModels(TestCase):
    def test_manufacturer_model_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="USA"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}"
        )

    def test_driver_model_str(self):
        driver = get_user_model().objects.create_user(
            username="test user",
            password="password123",
            license_number="ABC12345"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})"
        )

        self.assertEqual(driver.username, "test user")
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertTrue(driver.check_password("password123"))

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test user",
            password="password123",
            license_number="ABC12345"
        )

        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")
