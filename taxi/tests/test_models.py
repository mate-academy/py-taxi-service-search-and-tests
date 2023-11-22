from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Test", country="test")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self):
        name = "Test"
        country = "Test"
        model = "Test"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        license_number = "TEST11111"
        username = "username"
        password = "test123"
        first_name = "test2"
        last_name = "test3"

        driver = get_user_model().objects.create_user(
            license_number=license_number,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_driver_license_str(self):
        license_number = "TEST11111"
        username = "username"
        password = "test123"
        driver = get_user_model().objects.create_user(
            license_number=license_number,
            username=username,
            password=password
        )
        self.assertEqual(driver.license_number, license_number)
