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
        driver = get_user_model().objects.create_user(
            username="test",
            license_number="XYZ123456",
            password="testpassword"
        )
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.license_number, "XYZ123456")
        self.assertTrue(driver.check_password("testpassword"))
