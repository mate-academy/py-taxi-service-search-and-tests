from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class DriverModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create(
            username="myuser",
            password="pass123test",
            first_name="my",
            last_name="user",
            email="user@user.com",
            license_number="ASD12345"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "myuser (my user)"
        )

    def test_create_driver_with_license(self):
        self.assertEqual(
            self.driver.license_number,
            "ASD12345"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            "/drivers/1/"
        )


class CarModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="myname",
            country="mycountry"
        )
        car = Car.objects.create(
            model="mymodel",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), "mymodel")


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="myname",
            country="mycountry"
        )
        self.assertEqual(
            str(manufacturer),
            "myname mycountry"
        )
