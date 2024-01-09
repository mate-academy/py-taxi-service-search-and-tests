from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )


class DriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            first_name="test_name",
            last_name="test_lastname",
            password="test_password",
            license_number="ABC12345"
        )

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, "test")
        self.assertTrue(self.driver.check_password("test_password"))
        self.assertTrue(self.driver.license_number, "ABC12345")

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )


class CarTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            first_name="test_name",
            last_name="test_lastname",
            password="test_password",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set((self.driver,))

    def test_car_str(self):
        self.assertEqual(
            str(self.car),
            self.car.model
        )
