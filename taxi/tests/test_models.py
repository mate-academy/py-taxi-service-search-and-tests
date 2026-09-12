from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="USA",
        )
        self.driver = Driver.objects.create_user(
            username="TestUser",
            first_name="John",
            last_name="Doe",
            password="test1234",
            license_number="1234",
        )

    def test_manufacture_str(self):
        self.assertEqual(str(self.manufacturer), "Manufacturer USA")

    def test_car_str(self):
        car = Car.objects.create(
            model="Car",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), "Car")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "TestUser (John Doe)")

    def test_if_password_is_valid(self):
        self.assertTrue(self.driver.check_password("test1234"))
