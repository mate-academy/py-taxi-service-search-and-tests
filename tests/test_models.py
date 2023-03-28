from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Jeep", country="USA")
        self.assertEqual(
            str(manufacturer), "Jeep USA"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test1234",
            first_name="test_name",
            last_name="test_last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Jeep", country="USA")
        car = Car.objects.create(model="Jeep", manufacturer=manufacturer)
        self.assertEqual(
            str(car), car.model
        )
