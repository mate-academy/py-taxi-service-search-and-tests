from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import (Manufacturer,
                         Car)


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            first_name="Test",
            last_name="TestL"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)
