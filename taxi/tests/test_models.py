from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test username",
            password="12345",
            first_name="test first name",
            last_name="test last name",
            license_number="YFT12345",
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)
        self.assertEqual(str(car), car.model)

    def test_driver_license_num(self):
        self.assertEqual(self.driver.username, "test username")
        self.assertEqual(self.driver.license_number, "YFT12345")
        self.assertTrue(self.driver.check_password("12345"))

    def test_get_driver_absolute_url(self):
        url = reverse("taxi:driver-detail", args=[self.driver.id])
        self.assertEqual(self.driver.get_absolute_url(), url)
