from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class TestCarModel(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry",
        )
        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)


class TestManufacturerModel(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry",
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class TestDriverModel(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="TestUser1",
            password="TestPassword1",
            first_name="TestFirstName1",
            last_name="TestLastName1",
            license_number="AAA12345",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_driver_attrs(self):
        self.assertEqual(self.driver.username, "TestUser1")
        self.assertEqual(self.driver.license_number, "AAA12345")
        self.assertTrue(self.driver.check_password("TestPassword1"))
