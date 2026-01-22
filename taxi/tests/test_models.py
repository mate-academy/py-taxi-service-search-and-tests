from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelTestCase(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="tests",
                                                   country="testcountry")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="tests",
            country="testcountry"
        )
        driver = Driver.objects.create(license_number="testlicense")
        car = Car.objects.create(model="testcar", manufacturer=manufacturer)
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="testuser", first_name="testfirst", last_name="testlast"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})",
        )

    def test_driver_with_license_number(self):
        license_number = "testlicense"
        username = "testuser"
        first_name = "testfirst"
        last_name = "testlast"
        password = "PASSWORD"
        driver = get_user_model().objects.create_user(
            license_number=license_number,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
