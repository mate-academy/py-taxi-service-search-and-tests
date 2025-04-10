from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Test", country="US")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_car(self):
        manufacturer = Manufacturer.objects.create(name="Test", country="123")
        car = Car.objects.create(model="TT", manufacturer=manufacturer)
        self.assertEqual(car.model, "TT")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test",
            first_name="Test_first",
            last_name="Test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_driver_licence(self):
        username = "Test"
        email = "mail@m.ii"
        first_name = "Test_first"
        last_name = "Test_last"
        license_number = "TTT11111"
        password = "test123"
        driver = get_user_model().objects.create(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
