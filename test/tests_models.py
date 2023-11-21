from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name}"
                         f" {manufacturer.country}")

    def test_driver_str(self):
        username = "test"
        first_name = "test_first"
        last_name = "last_name"
        license_number = "AAA12345"
        password = "password"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
            password=password,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        car = Car.objects.create(model="test_model",
                                 manufacturer=manufacturer)
        self.assertEqual(
            str(car),
            f"{car.model} {car.manufacturer.name}")
