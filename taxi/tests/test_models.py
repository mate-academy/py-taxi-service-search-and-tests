from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    def test_manufacturer_model_str_method(self):
        manufacturer = Manufacturer.objects.create(name="test", country="Test")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_model_str_method(self):
        driver = Driver.objects.create(
            username="Test",
            password="test123",
            first_name="test_first",
            last_name="test_second"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_model_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Test"
        )
        driver = Driver.objects.create(
            username="Test",
            password="test123",
            first_name="test_first",
            last_name="test_second"
        )
        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(
        self
    ):
        driver = get_user_model().objects.create_user(
            username="Test",
            password="test123",
            first_name="test_first",
            last_name="test_second",
            license_number="ADM56984",
        )
        self.assertEqual(driver.username, "Test")
        self.assertTrue(driver.check_password("test123"))
        self.assertEqual(driver.first_name, "test_first")
        self.assertEqual(driver.last_name, "test_second")
        self.assertEqual(driver.license_number, "ADM56984")
