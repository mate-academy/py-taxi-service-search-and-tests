from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Corolla", manufacturer=manufacturer)
        self.assertEqual(str(car), "Corolla")

    def test_driver_license_number(self):
        driver = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="ABC12345"
        )
        self.assertIsNotNone(driver.id)
        self.assertEqual(driver.username, "testuser")
        self.assertTrue(driver.check_password("password123"))
        self.assertEqual(driver.license_number, "ABC12345")
