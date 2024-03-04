from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="German"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model()
        test_driver = driver.objects.create_user(
            username="Test",
            password="test123",
            first_name="test_first",
            last_name="test_last"
        )
        self.assertEqual(
            str(test_driver),
            f"{test_driver.username} "
            f"({test_driver.first_name} {test_driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="German"
        )
        car = Car.objects.create(model="Cadet", manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license(self):
        username = "Test"
        password = "test123"
        license_number = "Test_number"

        driver = get_user_model()
        test_driver = driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(test_driver.username, username)
        self.assertEqual(test_driver.license_number, license_number)
        self.assertTrue(test_driver.check_password(password))
