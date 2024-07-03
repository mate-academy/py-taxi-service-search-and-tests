from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="Test1"
        )
        self.driver = Driver.objects.create_user(
            username="test",
            password="Test123",
            license_number="LCN54321"
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_create_driver_with_license_number(self):
        driver_with_license = Driver.objects.create_user(
            username="driver license",
            password="passtest",
            license_number="ABC12345"
        )
        self.assertEqual(driver_with_license.license_number, "ABC12345")
        self.assertEqual(driver_with_license.username, "driver license")
