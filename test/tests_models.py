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
        driver_data = {
            "username": "test",
            "first_name": "test_first",
            "last_name": "last_name",
            "license_number": "AAA12345",
            "password": "password",
        }

        driver = get_user_model().objects.create_user(**driver_data)

        self.assertEqual(driver.username, driver_data["username"])
        self.assertEqual(driver.first_name, driver_data["first_name"])
        self.assertEqual(driver.last_name, driver_data["last_name"])
        self.assertEqual(driver.license_number, driver_data["license_number"])
        self.assertTrue(driver.check_password(driver_data["password"]))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        car = Car.objects.create(model="test_model",
                                 manufacturer=manufacturer)
        self.assertEqual(
            str(car),
            f"{car.model} {car.manufacturer.name}"
        )
