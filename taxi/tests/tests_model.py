from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name", country="Test country"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="Test 12345",
            first_name="test first",
            last_name="test last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name", country="Test country"
        )
        car = Car.objects.create(model="test model", manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")

    def test_driver_license(self):
        driver = get_user_model().objects.create_user(
            username="test username",
            password="Test 12345",
            license_number="Test License",
        )
        self.assertEqual(driver.license_number, "Test License")
        self.assertEqual(driver.username, "test username")
        self.assertTrue(driver.check_password("Test 12345"))
