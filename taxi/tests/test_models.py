from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )

        self.driver = get_user_model().objects.create_user(
            username="TestName",
            password="Password111",
            first_name="TestFirst",
            last_name="TestLast",
            license_number="LIC12345",
        )

        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
