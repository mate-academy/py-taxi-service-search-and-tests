from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Test Name",
                                                   country="Test Country",)
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test Username",
            first_name="test first",
            last_name="test last",
            password="testpassword"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )

        user = get_user_model().objects.create_user(
            username="Test Username",
            first_name="test first",
            last_name="test last",
            password="testpassword"
        )

        car = Car.objects.create(
            manufacturer=manufacturer,
            model="Test Model",
        )

        car.drivers.add(user)

        self.assertEqual(str(car), "Test Model")
