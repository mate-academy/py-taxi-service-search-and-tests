from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    username = "test_user"
    password = "test_password"
    license_number = "ABC123"

    @classmethod
    def setUp(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="test",
            country="TEST"
        )
        cls.driver = get_user_model().objects.create_user(
            username=cls.username,
            password=cls.password,
            first_name="John",
            last_name="Doe",
            license_number=cls.license_number
        )
        cls.car = Car.objects.create(model="test",
                                     manufacturer=cls.manufacturer)
        cls.car.drivers.set([cls.driver])

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer),
                         f"{self.manufacturer.name} "
                         f"{self.manufacturer.country}")

    def test_driver_create_with_license_number(self):
        self.assertEqual(self.driver.license_number,
                         self.license_number)

    def test_driver_username(self):
        self.assertEqual(self.driver.username, self.username)

    def test_driver_password(self):
        self.assertTrue(self.driver.check_password(self.password))

    def test_driver_str(self):
        self.assertEqual(str(self.driver),
                         f"{self.driver.username} "
                         f"({self.driver.first_name} "
                         f"{self.driver.last_name})")

    def test_car_str(self):
        self.assertEqual(str(self.car), "test")
