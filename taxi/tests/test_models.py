from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.driver = Driver.objects.create(
            username="test_user",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="TSE10000"
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEquals(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self):
        self.assertEquals(str(self.car), self.car.model)

    def test_driver_str(self):
        self.assertEquals(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name} {self.driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "test_user1"
        password = "test_password"
        license_number = "XXX10000"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
