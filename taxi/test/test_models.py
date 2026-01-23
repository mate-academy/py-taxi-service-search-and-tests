from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


# Create your tests here.
class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(name="test", country="test_country")
        self.assertEqual(str(manufacturer), "test test_country")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer(name="test", country="test_country")
        car = Car(model="test_model", manufacturer=manufacturer)
        self.assertEqual(str(car), "test_model")

    def test_create_driver_with_license_number(self):
        license_number = "00test"
        username = "test"
        password = "<PASSWORD>"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
