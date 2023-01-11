from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda", country="Japan"
        )

        self.assertEqual(str(manufacturer), "Mazda Japan")


class DriverModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create(
            username="user",
            password="userpassword",
            first_name="John",
            last_name="Black",
            email="johnblack@gmail.com",
            license_number="ASD12345"
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "user (John Black)")

    def test_create_driver_with_license(self):
        self.assertEqual(self.driver.license_number, "ASD12345")

    def test_driver_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")


class CarModelTests(TestCase):

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mitsubishi",
            country="Japan"
        )
        car = Car.objects.create(
            model="Lancer",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), "Lancer")
