from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


# Create your tests here.
class ModelsTestCase(TestCase):
    def test_manufacturer_str_and_dani(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )
        self.assertEqual(manufacturer.name, "test")
        self.assertEqual(manufacturer.country, "Ukraine")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Ukraine",
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "test")

    def test_driver_str_and_dani(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
            license_number="GFR12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username}"
            f" ({driver.first_name}"
            f" {driver.last_name})"
        )
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.first_name, "test_first")
        self.assertEqual(driver.last_name, "test_last")
        self.assertEqual(driver.license_number, "GFR12345")
        self.assertTrue(driver.check_password("test1234"))
