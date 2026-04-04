from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        name = "Test_name"
        country = "Test_country"

        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_str_password_lisense(self):
        username = "Test_username"
        first_name = "Test_first"
        last_name = "Test_last"
        password = "Test_12345"
        license_number = "GTR12345"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        model = "Test_model"
        manufacturer = Manufacturer.objects.create(
            name="Test_manufacturer",
            country="Test_country",
        )
        car = Car.objects.create(model=model, manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
