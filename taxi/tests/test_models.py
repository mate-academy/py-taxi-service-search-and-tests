from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Country"
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            license_number="ASC12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url_for_driver(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")
