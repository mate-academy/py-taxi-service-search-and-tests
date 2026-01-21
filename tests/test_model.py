from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        name = "BMW"
        country = "Germany"
        self.manufacturer = Manufacturer.objects.create(name=name, country=country)

    def test_str(self):
        self.assertEqual(
            self.manufacturer.__str__(),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )


class DriverModelTest(TestCase):
    def setUp(self):
        username = "Admin"
        password = "<PASSWORD>"
        license_number = "LAT12345"
        first_name = "John"
        last_name = "Doe"
        self.driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
        )

    def test_str(self):
        self.assertEqual(
            self.driver.__str__(),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})",
        )


class CarModelTest(TestCase):
    def setUp(self):
        name = "BMW"
        country = "Germany"
        self.manufacturer = Manufacturer.objects.create(name=name, country=country)
        username = "Admin"
        password = "<PASSWORD>"
        license_number = "LAT12345"
        first_name = "John"
        last_name = "Doe"
        self.driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
        )
        self.car = Car.objects.create(
            model="X6",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver])

    def test_str(self):
        self.assertEqual(self.car.__str__(), self.car.model)
