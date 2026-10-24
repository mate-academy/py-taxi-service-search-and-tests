from django.test import TestCase

from taxi.models import Manufacturer, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test_username",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            license_number="TST12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_create(self):
        username = "test_username"
        password = "test123"
        first_name = "test_first"
        last_name = "test_last"
        license_number = "TST12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
