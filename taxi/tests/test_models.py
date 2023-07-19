from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import (
    Manufacturer,
    Car,
)


class ModelsTest(TestCase):

    def test_manufacturers(self):
        name = "test",
        country = "TestCountry"
        manufacturer = Manufacturer(
            name=name,
            country=country
        )
        self.assertEquals(str(manufacturer), f"{name} {country}")

    def test_cars(self):
        model = " test"
        manufacturer = Manufacturer(
            name="test_manufacturer",
            country="TestCountry"
        )

        car = Car(
            model=model,
            manufacturer=manufacturer
        )
        self.assertEquals(str(car), f"{model}")

    def test_drivers_str(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
            license_number="TES12345"
        )

        self.assertEquals(str(driver), "test_driver (test_fn test_ln)")

    def test_crete_drivers_license_number(self):
        username = "test_driver"
        password = "test_pass123"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)
