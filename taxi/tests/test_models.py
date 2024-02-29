from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="Test",
            last_name="Driver",
            password="1234test",
            license_number="ABC12345"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_driver_license_number(self):
        self.assertEqual(
            self.driver.license_number,
            "ABC12345"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            "/drivers/1/"
        )


class CarModelTest(TestCase):
    def test_car_str(self):
        car = Car.objects.create(
            model="i8",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            )
        )

        self.assertEqual(str(car), car.model)
