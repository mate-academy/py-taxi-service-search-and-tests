from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class TestModels(TestCase):
    def test_manufacturers_str(self):
        manufacturers = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        self.assertEqual(
            str(manufacturers),
            f"{manufacturers.name} {manufacturers.country}"
        )

    def test_drivers_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            license_number="test_license_number",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturers = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturers
        )
        self.assertEqual(
            str(car),
            car.model,
        )
