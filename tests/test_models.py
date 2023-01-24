from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} ({manufacturer.country})"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.assertEqual(str(driver), driver.username)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "RDM12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test_country"
        )
        car = Car.objects.create(
            model="test model", manufacturer=manufacturer
        )
        if manufacturer.name.split()[0] in car.model:
            self.assertEqual(str(car), car.model)
        else:
            self.assertEqual(str(car), f"{car.manufacturer.name} {car.model}")
