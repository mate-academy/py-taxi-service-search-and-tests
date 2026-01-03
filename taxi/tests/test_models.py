from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTestCase(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW_test1",
            country="Germany",
        )
        self.assertEqual(str(manufacturer), "BMW_test1 Germany")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="password123",
            license_number="ABC12345",
            first_name="Test",
            last_name="Driver",
        )
        self.assertEqual(str(driver), "test_driver (Test Driver)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi_test2",
            country="Germany",
        )
        car = Car.objects.create(
            model="A6",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "A6")

    def test_driver_create_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="user1",
            password="StrongPass123",
            license_number="LIC12345",
        )
        self.assertEqual(driver.license_number, "LIC12345")
        self.assertTrue(driver.check_password("StrongPass123"))
