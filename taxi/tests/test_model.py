from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ModelTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="testfirst",
            last_name="testlast",
            password="test123",
            license_number="ASD12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="testbmw",
            country="Ukraine",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        driver = Driver.objects.create(
            username="testuser",
            license_number="ASD12345"
        )
        bmw = Manufacturer.objects.create(name="BMW", country="Ukraine")
        car = Car.objects.create(model="testbmw", manufacturer=bmw)
        car.drivers.add(driver)

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "ASD12345"
        author = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(author.username, username)
        self.assertEqual(author.license_number, license_number)
        self.assertTrue(author.check_password(password))
