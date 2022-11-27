from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="test first",
            last_name="test last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} " f"{driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            id=1,
            username="test",
            password="test123",
            first_name="test first",
            last_name="test last",
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        car = Car.objects.create(model="test", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
