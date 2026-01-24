from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test123",
            license_number="FFF00000"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="TestUA"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="TestMW",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(
            str(car),
            car.model
        )
