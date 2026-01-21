from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="ManufacturerTest", country="TestCountry"
        )
        self.assertEqual(str(manufacturer), "ManufacturerTest TestCountry")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="ManufacturerTest", country="TestCountry"
        )
        car = Car.objects.create(manufacturer=manufacturer, model="TestModel")
        self.assertEqual(str(car), "TestModel")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
            first_name="TestFirstName",
            last_name="TestLastName",
            license_number="TES32288",
        )
        self.assertEqual(str(driver), "TestUser (TestFirstName TestLastName)")

    def test_driver_url(self):
        driver = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
            first_name="TestFirstName",
            last_name="TestLastName",
            license_number="TES32288",
        )
        self.assertEqual(
            str(driver.get_absolute_url()), f"/drivers/{driver.id}/"
        )
