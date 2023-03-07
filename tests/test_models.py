from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class DriverModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create(
            username="BigBob",
            password="passpasspass",
            first_name="Big",
            last_name="Bob",
            email="Bigbob1967@gmail.com",
            license_number="QWE12345"
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "BigBob (Big Bob)")

    def test_create_driver_with_license(self):
        self.assertEqual(self.driver.license_number, "QWE12345")

    def test_driver_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")


class CarModelTests(TestCase):

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), "Corolla")


class ManufacturerModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.assertEqual(str(manufacturer), "Tesla USA")
