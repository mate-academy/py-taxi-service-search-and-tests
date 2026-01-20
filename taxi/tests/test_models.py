from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestManufacturerModel(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Country",
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class TestDriverModel(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test123",
            password="Testpass123",
            first_name="Test_first",
            last_name="Test_second",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_driver_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.id}/"
        )

    def test_create_driver_with_driver_license(self):
        username = "Test license"
        password = "Testpass123"
        license_number = "TST12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))


class TestCarModel(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Country",
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
