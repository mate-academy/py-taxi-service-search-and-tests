from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test", country="test country"
        )
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test12345",
            first_name="test first",
            last_name="test last",
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        self.assertEquals(self.driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        car = Car.objects.create(
            model="test car",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)
