from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Seat", country="Spain")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Seat", country="Spain")
        car = Car.objects.create(model="Lion", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="admin",
            first_name="Jhon",
            last_name="Smith",
            license_number="ABC12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username}" f" "
            f"({driver.first_name}" f" {driver.last_name})",
        )

    def test_driver_create_with_license_number(self):
        username = "admin"
        password = "12345@"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
