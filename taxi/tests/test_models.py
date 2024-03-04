from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test",
            password="Test-password",
            first_name="John",
            last_name="Smith",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name}"
            f" {driver.last_name})"
        )

    def test_create_driver_with_license(self):
        password = "Test-password"
        hashed_password = make_password(password)
        driver = get_user_model().objects.create(
            username="Test",
            password=hashed_password,
            license_number="ABC12345",
        )
        self.assertEqual(driver.username, "Test")
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertTrue(driver.check_password(password))
