from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import (
    Manufacturer,
    Driver,
    Car
)


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country"
        )
        expected_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_str)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Driver",
            first_name="First",
            last_name="Last",
            password="<PASSWORD>"
        )
        expected_str = (f"{driver.username} "
                        f"({driver.first_name} {driver.last_name})")
        self.assertEqual(str(driver), expected_str)
        self.assertEqual(driver.password, "<PASSWORD>")

    def test_driver_license_number(self):
        driver = get_user_model().objects.create_user(
            username="Driver",
            first_name="First",
            last_name="Last",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver.license_number), "ABC12345")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country"
        )
        car = Car.objects.create(model="Model", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
