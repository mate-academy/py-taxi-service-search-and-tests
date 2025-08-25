from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        self.assertEqual(
            str(car),
            car.model
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            license_number="TES12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolut_url(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            license_number="TES12345"
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
