from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        username = "test_username"
        first_name = "test_first_name"
        last_name = "test_last_name"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(str(driver), f"{username} ({first_name} {last_name})")

    def test_car_str(self):
        name = "test_name"
        country = "test_country"
        model = "test_model"

        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), model)

    def test_create_driver_with_license(self):
        username = "test_username"
        password = "test_pass"
        first_name = "test_first_name"
        last_name = "test_last_name"
        license_number = "AAA11111"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
