from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


# Create your tests here.
class ModelsTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="test",
            password="test12345",
            first_name="test_first",
            last_name="test_last",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="test_country"
        )

    def test_manufacturer_str(self):
        manufacturer = self.manufacturer
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        driver = self.driver
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        car = Car.objects.create(
            model="test_model", manufacturer=self.manufacturer
        )
        car.drivers.add(self.driver)
        self.assertEqual(str(car), car.model)
