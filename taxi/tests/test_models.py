from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany")

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany")
        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), f"{car.model}")
