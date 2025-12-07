from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ModelTests(TestCase):
    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Test1",
            password="password1234",
            first_name="Test",
            last_name="Test2",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country"
        )
        driver = Driver.objects.create(
            username="Testuser",
            license_number="ASD12345"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_driver_with_license_number(self):
        username = "test"
        password = "password1234"
        license_number = "ASD12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
