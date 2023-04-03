from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Nimbus",
            country="UK"
        )
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test1234",
            first_name="Te",
            last_name="St",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=Manufacturer.objects.get(pk=1)
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, "Test")
        self.assertTrue(self.driver.check_password("test1234"))
        self.assertEqual(self.driver.license_number, "ABC12345")

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
