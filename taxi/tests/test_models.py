from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def test_drivers_str(self):
        drivers = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            license_number="Test License",
            first_name="Test_first",
            last_name="Test_last",
        )
        self.assertEqual(
            str(drivers),
            f"{drivers.username} ({drivers.first_name} {drivers.last_name})"
        )

    def test_manufacturers_str(self):
        manufacturers = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        self.assertEqual(
            str(manufacturers),
            f"{manufacturers.name} {manufacturers.country}"
        )

    def test_cars_str(self):
        manufacturers = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        cars = Car.objects.create(
            model="test_model",
            manufacturer=manufacturers,
        )
        self.assertEqual(str(cars), f"{cars.model}")
