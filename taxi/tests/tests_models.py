from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country")
        expected_str = "test test_country"
        self.assertEqual(str(manufacturer), expected_str)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="tname",
            last_name="lname",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test_country")
        car = Car.objects.create(model="Tesla",
                                 manufacturer=manufacturer)
        self.assertEqual(str(car),
                         car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "LWE12332"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
