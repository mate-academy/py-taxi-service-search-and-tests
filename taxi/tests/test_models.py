from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
       manufacturer = Manufacturer.objects.create(name="Test", country="US")
       expected_str = "Test US"
       self.assertEqual(str(manufacturer), expected_str)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Test", country="US")
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(
            str(driver),
    f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
