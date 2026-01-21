from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer_ = Manufacturer.objects.create(name="test")

        self.assertEqual(
            str(manufacturer_),
            f"{manufacturer_.name} {manufacturer_.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )

        self.assertEqual(
            str(driver), f"{driver.username} "
                         f"({driver.first_name} "
                         f"{driver.last_name})"
        )

    def test_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "Test license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
