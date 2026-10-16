from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        self.assertEqual(str(driver), "test_user (John Doe)")

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            license_number="ABC12345",
        )
        self.assertEqual(
            driver.get_absolute_url(), f"/drivers/{driver.pk}/"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Camry")

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            license_number="ABC12345",
        )
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertTrue(driver.check_password("test12345"))
