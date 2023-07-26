from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword",
            license_number="TestLicenseNumber",
            first_name="TestFirstName",
            last_name="TestLastName"
        )

    def test_manufacturer_str_method(self):
        self.assertEquals(str(self.manufacturer), "TestName TestCountry")

    def test_car_str_method(self):
        self.assertEquals(str(self.car), "TestModel")

    def test_driver_str_method(self):
        self.assertEquals(
            str(self.driver),
            "TestUsername (TestFirstName TestLastName)"
        )

    def test_get_absolute_url_for_driver(self):
        self.assertEquals(self.driver.get_absolute_url(), "/drivers/1/")
