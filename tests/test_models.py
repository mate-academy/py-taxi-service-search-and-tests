from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry"
        )
        car = Car.objects.create(model="TestModel", manufacturer=manufacturer)
        self.assertEqual(
            str(car),
            car.model
        )

    def test_create_driver_with_license_number(self):
        username = "Test"
        password = "Test1234"
        license_number = "TestLicenseNumber"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
