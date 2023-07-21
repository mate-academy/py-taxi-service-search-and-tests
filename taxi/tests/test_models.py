from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )

        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}"
                         )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="first",
            last_name="last",
        )

        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name} {driver.last_name})"
                         )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )

        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)
