from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car

User = get_user_model()


class ModelTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = User.objects.create_user(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "driver1"
        password = "password123"
        license_number = "ABC12345"
        driver = User.objects.create_user(
            username=username,
            password=password,
            license_number=license_number

        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
