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
        manufacturer = self.manufacturer
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        driver = self.driver
        self.assertEqual(driver.username, "Test")
        self.assertTrue(driver.check_password("test1234"))
        self.assertEqual(driver.license_number, "ABC12345")

    def test_car_str(self):
        car = self.car
        self.assertEqual(str(self.car), car.model)
