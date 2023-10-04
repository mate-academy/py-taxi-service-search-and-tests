from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_license_num(self):
        username = "Test name"
        password = "test1234"
        license_num = "ABG46739"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_num
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_num)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
        )
        driver = get_user_model().objects.create_user(
            username="Test name",
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )
        driver.cars.add(car)
        self.assertEqual(str(car), car.model)
        self.assertTrue(
            car.drivers.filter(username=driver.username).exists()
        )
        self.assertEqual(car.manufacturer.name, manufacturer.name)
