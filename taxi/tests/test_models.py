from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="test_name", country="test_country")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test_username",
            first_name="first_name",
            last_name="last_name",
            license_number="DSA12345",
            password="test123"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.username, "test_username")
        self.assertEqual(driver.first_name, "first_name")
        self.assertEqual(driver.last_name, "last_name")
        self.assertEqual(driver.license_number, "DSA12345")
        self.assertTrue(driver.check_password("test123"))


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="test_name", country="test_country")
        Car.objects.create(
            model="test_model",
            manufacturer_id=1
        )

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)
