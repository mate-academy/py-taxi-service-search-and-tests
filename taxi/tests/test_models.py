from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="test first",
            last_name="test last",
            password="test1234",
            license_number="ABC12345"

        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set = [self.driver.pk]

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        absolute_url = f"/drivers/{self.driver.pk}/"
        self.assertEqual(url, absolute_url)
