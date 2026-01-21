from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class TestModels(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="test123123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="test_license_number",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )

        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="test_model",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name}"
            f" {self.driver.last_name})"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self):
        self.assertEqual(
            str(self.car), f"{self.car.model}"
        )

    def test_driver_number_license_create(self):
        self.assertEqual(self.driver.username, "test_user")
        self.assertTrue(self.driver.check_password("test123123"))
        self.assertEqual(self.driver.license_number, "test_license_number")

    def test_driver_get_absolute_url(self):
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk})
        self.assertEqual(self.driver.get_absolute_url(), expected_url)
