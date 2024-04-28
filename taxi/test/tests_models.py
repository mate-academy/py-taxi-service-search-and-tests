from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_state")
        self.assertEqual(str(manufacturer), manufacturer.name)

    def test_driver_str(self):
        driver_test = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",

        )
        self.assertEqual(
            str(driver_test),
            f"{driver_test.username}: "
            f"{driver_test.first_name} {driver_test.last_name}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_state"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_create_car_with_lisence_number(self):
        username = "test"
        password = "test123"
        license_number = "TES12345"
        driver_test = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number

        )
        self.assertEqual(driver_test.username, username)
        self.assertTrue(driver_test.check_password(password))
        self.assertEqual(driver_test.license_number, license_number)
