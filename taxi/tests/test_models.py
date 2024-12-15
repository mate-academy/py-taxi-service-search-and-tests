from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test Driver",
            first_name="test first",
            last_name="test last",
            password="test123",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        car = Car.objects.create(model="Test Model", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_creat_driver_with_license(self):
        username = "Test Driver"
        license_number = "VVV12345"
        password = "test123"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            password=password,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
