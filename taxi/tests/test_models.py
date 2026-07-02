from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="TEST")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            first_name="test",
            last_name="test",
            email="test@test.tes",
            password="Test123",
            license_number="TES12345",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="TEST")
        driver = get_user_model().objects.create(
            first_name="test",
            last_name="test",
            email="test@test.tes",
            password="Test123",
            license_number="TES12345",
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), "test")

    def test_driver_license_number(self):
        driver = get_user_model().objects.create_user(
            first_name="test",
            last_name="test",
            username="test",
            email="test@test.tes",
            password="Test123",
            license_number="TES12345",
        )
        self.assertEqual(driver.license_number, "TES12345")
        self.assertEqual(driver.first_name, "test")
        self.assertEqual(driver.last_name, "test")
        self.assertEqual(driver.email, "test@test.tes")
        self.assertTrue(driver.check_password("Test123"))
        self.assertEqual(driver.username, "test")
