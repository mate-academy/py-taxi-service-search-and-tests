from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Jaguar",
            country="USD"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTests(TestCase):
    #
    def setUp(self):
        self.username = "test"
        self.password = "<PASSWORD>"
        self.license_number = "1234567890"
        self.driver = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            license_number=self.license_number,
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertEqual(self.driver.license_number, self.license_number)
        self.assertTrue(self.driver.check_password(self.password))


class CarModelTests(TestCase):

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Jaguar",
            country="USD"
        )
        car = Car.objects.create(model="DEO", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
