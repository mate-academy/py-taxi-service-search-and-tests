from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = (
            Manufacturer.objects.create(name="test", country="second_test")
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test_passw123",
            first_name="first_test",
            last_name="second_test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_car_str(self):
        manufacturer = (
            Manufacturer.objects.create(name="test", country="second_test")
        )

        car_model = (
            Car.objects.create(model="test_model", manufacturer=manufacturer)
        )

        self.assertEqual(str(car_model), car_model.model)

    def test_create_driver_with_license_plate_number(self):
        username = "test"
        password = "test_passw123"
        license_number = "new_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
