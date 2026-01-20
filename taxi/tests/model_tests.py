from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car

DRIVER_ABSOLUTE_URL = "drivers/1/"


class ModelTest(TestCase):
    def test_car_string_gives_correct_result(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="USA"
        )
        car = Car.objects.create(
            model="test1",
            manufacturer=manufacturer
        )
        self.assertEqual(car, "test1")

    def test_driver_returns_correct_path(self):
        driver = get_user_model().objects.create_user(
            username="user",
            password="pass"
        )
        self.assertEqual(driver.get_absolute_url(), DRIVER_ABSOLUTE_URL)
