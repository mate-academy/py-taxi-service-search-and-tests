from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="VW",
            country="Germany"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Username",
            password="Password",
            first_name="First Name",
            last_name="Last Name"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="VW",
            country="Germany"
        )
        car = Car.objects.create(model="T5", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_licence(self):
        driver = get_user_model().objects.create_user(
            username="Username",
            password="Password",
            first_name="First Name",
            last_name="Last Name",
            license_number="ABC12345",
        )

        self.assertEqual(driver.license_number, "ABC12345")
        self.assertTrue(driver.check_password("Password"))
        self.assertEqual(driver.username, "Username")
        self.assertEqual(driver.first_name, "First Name")
        self.assertEqual(driver.last_name, "Last Name")
