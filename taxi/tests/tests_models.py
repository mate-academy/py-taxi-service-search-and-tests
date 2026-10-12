from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        self.assertEqual(str(manufacturer), "test_name test_country")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email",
        )

        self.assertEqual(
            str(driver),
            "test_username (test_first_name test_last_name)"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)

        self.assertEqual(str(car), "test_model")

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test_password"
        license_number = "AAA11111"

        driver = get_user_model().objects.create_user(
            username=username,
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email",
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
