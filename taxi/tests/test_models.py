from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Testing"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="testname",
            first_name="first first",
            last_name="Test last",
            password="test1234",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_licence_number(self):
        """test that driver creates with license_number"""
        username = "username"
        password = "pass1234"
        license_number = "NUM12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_test_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="Test",
            country="Testing")

        car = Car.objects.create(
            model="Test Volvo",
            manufacturer=manufacturer_,
        )
        self.assertEqual(str(car), car.model)
