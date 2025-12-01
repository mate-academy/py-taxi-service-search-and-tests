from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            password="test1234",
            username="test username",
            first_name="test first name",
            last_name="test last name",
            license_number="DFD45454"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country",
        )
        driver = Driver.objects.create_user(
            password="test1234",
            username="test username",
            first_name="test first name",
            last_name="test last name",
            license_number="DFD45454"
        )
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_licence_number(self):
        driver = Driver.objects.create_user(
            password="test1234",
            username="test username",
            first_name="test first name",
            last_name="test last name",
            license_number="DFD45454"
        )
        self.assertEqual(driver.username, "test username")
        self.assertEqual(driver.license_number, "DFD45454")
