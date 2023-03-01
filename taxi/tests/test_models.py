from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="Test",
            password="Test12345",
            first_name="Ivan",
            last_name="Ivanenko",
            license_number="ABC12345"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license_number(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.license_number, "ABC12345")


class CarModelTest(TestCase):

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)
