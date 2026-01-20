from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver


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
        driver = Driver.objects.create(
            username="test",
            first_name="test first",
            last_name="test last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_create_with_licence_number(self):
        driver_data = {
            "username": "test",
            "license_number": "XYZ123456",
            "password": "testpassword"
        }

        driver = get_user_model().objects.create_user(**driver_data)

        self.assertEqual(driver.username, driver_data["username"])
        self.assertEqual(driver.license_number, driver_data["license_number"])
        self.assertTrue(driver.check_password(driver_data["password"]))
