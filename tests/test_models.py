from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import (
    Manufacturer,
    Car
)


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        name = "test_name"
        country = "test_country"
        manufacturer = Manufacturer(
            name=name,
            country=country
        )

        self.assertEqual(str(manufacturer), f"{name} {country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
            license_number="TES12345"
        )

        self.assertEqual(str(driver), "test_driver (test_fn test_ln)")

    def test_car_str(self):
        manufacturer = Manufacturer(
            name="test_name",
            country="test_country"
        )

        car = Car(model="test_model", manufacturer=manufacturer)

        self.assertEqual(str(car), "test_model")

    def test_create_driver_with_license_num(self):
        username = "test"
        password = "test123456"
        license_number = "LIS123456"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123456",
        )

        absolute_url = driver.get_absolute_url()

        self.assertEquals(absolute_url, f"/drivers/{driver.id}/")
