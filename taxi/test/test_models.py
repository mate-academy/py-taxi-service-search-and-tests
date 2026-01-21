from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="TEST")
        self.assertEqual(str(
            manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            license_number="ASD12345",
            username="test",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(str(
            driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="TEST")
        driver_one = get_user_model().objects.create(
            license_number="ASD12345",
            username="test1",
            first_name="John1",
            last_name="Doe1",
        )
        driver_two = get_user_model().objects.create(
            license_number="ASD54321",
            username="test2",
            first_name="John2",
            last_name="Doe2",
        )
        car = Car(model="test123", manufacturer=manufacturer, id=1)
        car.drivers.add(driver_one)
        car.drivers.add(driver_two)
        car.save()
        self.assertEqual(str(car), car.model)

    def test_driver_with_license_number(self):
        license_number = "ASD12345"
        username = "test1"
        password = "<PASSWORD>"
        driver = get_user_model().objects.create_user(
            license_number=license_number,
            username=username,
            password=password,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
