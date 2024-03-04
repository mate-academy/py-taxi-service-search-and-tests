from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

        self.assertEqual(str(manufacturer), f"{manufacturer.name} "
                                            f"{manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )

        self.assertEqual(str(driver), f"{driver.username} "
                                      f"({driver.first_name} "
                                      f"{driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        car = Car.objects.create(
            model="Zaporogec Ushastiy",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "testDriver"
        password = "testDriver12345"
        license_number = "ADM56984"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
