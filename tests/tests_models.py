from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_cars_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country")

        cars = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

        self.assertEquals(str(cars), cars.model)

    def test_driver_format_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="987654321some_test",
            first_name="Kostya",
            last_name="Kononenko"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "987654321some_test"
        license_number = "ABCD1234"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
