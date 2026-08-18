from django.contrib.auth import get_user_model
from django.db.models import Model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="test country")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test", first_name="test_first", last_name="test_last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} " f"{driver.last_name})",
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test",
            manufacturer=Manufacturer.objects.create(
                name="test", country="test country"
            ),
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create(
            username="test_user",
            first_name="John",
            last_name="Doe",
            license_number="XYZ123",
        )
        self.assertEqual(driver.username, "test_user")
        self.assertEqual(driver.first_name, "John")
        self.assertEqual(driver.last_name, "Doe")
        self.assertEqual(driver.license_number, "XYZ123")
