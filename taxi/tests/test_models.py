from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Test",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            email="Test",
            password="test123",
            first_name="Test_first_name",
            last_name="Test_last_name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            f"{car.model}"
        )

    def test_create_driver_with_license(self):
        username = "test"
        password = "test123"
        license_number = "test_license"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            password=password,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
