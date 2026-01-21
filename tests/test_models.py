from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="TestCountry"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            password="test123",
            first_name="test1",
            last_name="test2"
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})")

    def test_create_driver_with_license(self):
        username = "Test"
        password = "test123"
        license_number = "1111"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
