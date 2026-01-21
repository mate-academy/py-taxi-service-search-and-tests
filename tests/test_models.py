from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

        self.assertEqual(str(manufacturer), f"{manufacturer.name} "
                                            f"{manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="bobius",
            password="123456te",
            first_name="Bob",
            last_name="Smith"
        )

        self.assertEqual(str(driver), f"{driver.username} "
                                      f"({driver.first_name} "
                                      f"{driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Country"
        )
        car = Car.objects.create(
            model="A6",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "bobius"
        password = "123456te"
        license_number = "AAA12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
