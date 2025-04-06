from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModel(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        self.assertEqual(str(manufacturer), "TestName TestCountry")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            first_name="TestFirstName",
            last_name="TestLastName",
            username="TestUsername",
            password="<PASSWORD>",
            license_number="TestLicenseNumber",
        )
        self.assertEqual(
            str(driver),
            "TestUsername (TestFirstName TestLastName)"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        car = Car.objects.create(model="TestModel", manufacturer=manufacturer)
        self.assertEqual(str(car), "TestModel")

    def test_driver_with_license_number(self):
        driver = Driver.objects.create_user(
            first_name="TestFirstName",
            last_name="TestLastName",
            username="TestUsername",
            password="<PASSWORD>",
            license_number="TestLicenseNumber",
        )
        self.assertEqual(driver.license_number, "TestLicenseNumber")
        self.assertEqual(driver.first_name, "TestFirstName")
        self.assertEqual(driver.last_name, "TestLastName")
        self.assertTrue(driver.check_password("<PASSWORD>"))
        self.assertEqual(driver.username, "TestUsername")
