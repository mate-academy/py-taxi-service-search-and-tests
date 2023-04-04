from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        car = Manufacturer.objects.create(name="Mazda", country="Japan")
        self.assertEqual(str(car), "Mazda Japan")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Voldemort",
            password="Ban12345",
            first_name="Tom",
            last_name="Riddle"
        )
        self.assertEqual(str(driver), "Voldemort (Tom Riddle)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        car = Car.objects.create(model="Model S", manufacturer=manufacturer)

        self.assertEqual(str(car), "Model S")

    def test_driver_with_license_number(self):
        username = "Voldemort"
        password = "ban12345"
        license_number = "ZXC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
