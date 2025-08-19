from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_manufacturer_str(self):
        manufacturer = self.manufacturer
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create_user(
            username="user123",
            password="pass1234",
            first_name="first",
            last_name="last"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        cls.car = Car.objects.create(
            model="Focus",
            manufacturer=cls.manufacturer
        )
        cls.car.drivers.add(cls.driver)

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = self.driver
        self.assertEqual(
            driver.get_absolute_url(),
            f"/drivers/{self.driver.pk}/"
        )

    def test_car_str(self):
        car = self.car
        self.assertEqual(str(car), self.car.model)
