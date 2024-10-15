from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "test_user"
        cls.license_number = "AAA00001"
        cls.password = "Password1!"
        cls.first_name = "James"
        cls.last_name = "Bond"
        cls.name = "BMW"
        cls.country = "Germany"
        cls.model = "M4"

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name=self.name,
            country=self.country,
        )
        self.assertEqual(str(manufacturer), f"{self.name} {self.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.assertEqual(
            str(driver),
            f"{self.username} ({self.first_name} {self.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name=self.name,
            country=self.country
        )
        car = Car.objects.create(
            model="M4",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), self.model)

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create(
            username=self.username,
            password=self.password,
            license_number=self.license_number
        )
        self.assertEqual(driver.license_number, self.license_number)
