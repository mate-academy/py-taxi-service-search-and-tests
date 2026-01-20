from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestsModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="Test")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            id="1",
            username="testname",
            first_name="first_test",
            last_name="last_test",
            license_number="HFJ12341"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test"
        )
        car = Car.objects.create(
            manufacturer=manufacturer,
            model="test",
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test3466"
        license_number = "HFJ12341"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
