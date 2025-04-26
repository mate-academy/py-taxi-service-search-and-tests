from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password",
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str_and_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name}"
            f")"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), f"{self.car.model}")

    def test_car_have_driver(self):
        self.assertIn(self.driver, self.car.drivers.all())
