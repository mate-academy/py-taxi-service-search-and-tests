from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Test", country="USA")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_t",
            password="1234",
            first_name="Test",
            last_name="Tester",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_cars_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test22",
            country="USA"
        )
        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            car.model
        )
