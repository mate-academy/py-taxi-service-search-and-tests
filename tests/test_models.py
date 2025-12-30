from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_Manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_Car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_Driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test username",
            password="Test password",
            first_name="Test first name",
            last_name="Test last name"
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_Driver_with_license_number(self):
        license_number = "Test license number"
        username = "Test username"
        password = "Test password"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
