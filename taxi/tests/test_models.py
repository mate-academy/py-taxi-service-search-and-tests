from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class DriverTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="driver",
            password="test1234",
            first_name=" Test first",
            last_name="Test last",
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_driver_license_number(self):
        username = "driver2"
        password = "password123"
        license_number = "XYZ12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        username = "driver3"
        password = "password345"
        license_number = "XYZ45678"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")


class CarTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)


class ManufacturerTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TOYOTA",
            country="Japan",
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")
