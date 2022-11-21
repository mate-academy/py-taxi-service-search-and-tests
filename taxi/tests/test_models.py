from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        name = "TestName"
        country = "TestCountry"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )

        self.assertEqual(str(manufacturer), f"{name} {country}")

    def test_driver_str(self):
        username = "Test1234"
        first_name = "TestName"
        last_name = "TestSurname"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(str(driver), f"{username} ({first_name} {last_name})")

    def test_create_driver(self):
        username = "Test1234"
        password = "TestPass"
        first_name = "TestName"
        last_name = "TestSurname"
        license_number = "TEST0123"
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

    def test_car_str(self):
        name = "TestName"
        country = "TestCountry"
        model = "TestModel"

        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), model)
