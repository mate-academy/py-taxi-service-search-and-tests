from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            (f"{manufacturer.name} "
             f"{manufacturer.country}")
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_1234"
        )
        self.assertEqual(
            str(driver),
            (f"{driver.username} "
             f"({driver.first_name} "
             f"{driver.last_name})")
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                name="test",
                country="test_country"
            )
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test_username"
        first_name = "test_first_name"
        last_name = "test_last_name"
        password = "test_1234"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))


