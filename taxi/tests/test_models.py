from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test username",
            password="test password",
            first_name="test first name",
            last_name="test last name",
            license_number="QAZ12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} {self.driver.last_name})")

    def test_car_str(self):
        car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.id}/"
        )
