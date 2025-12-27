from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Testname",
            country="Testcountry",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Testname",
            password="PASSWORD",
            first_name="Testfirst",
            last_name="Testlast",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Testname",
            country="Testcountry",
        )
        car = Car.objects.create(
            model="Testmodel",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_license_number(self):
        username = "Testname"
        password = "PASSWORD"
        license_number = "TTT45678"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.check_password(password), True)
