from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="GMC", country="USA")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="GMC", country="USA")
        car = Car.objects.create(model="Ford", manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            first_name="Test_first",
            last_name="Test_last",
            password="asdf1234*&^%",
            license_number="ASD12548"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license_exists(self):
        username = "test"
        password = "test12345"
        license_number = "DFS23415"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
