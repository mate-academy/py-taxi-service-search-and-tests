from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        car = Car.objects.create(model="Fiesta", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="testuser",
            first_name="Katya",
            last_name="Kilyk",
            license_number="ABC12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        password = "testpassword"
        driver = get_user_model().objects.create_user(
            username="testuser",
            first_name="Katya",
            last_name="Kilyk",
            license_number="ABC12345",
            password=password,
        )
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertEqual(driver.username, "testuser")
        self.assertTrue(driver.check_password(password))
