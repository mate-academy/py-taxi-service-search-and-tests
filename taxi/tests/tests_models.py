from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="uk")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Tester", first_name="Test", last_name="Tests"
        )
        self.assertEqual(
            str(driver), f"{driver.username} ({driver.first_name}"
                         f" {driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Test",
            manufacturer=Manufacturer.objects.create(name="test",
                                                     country="uk"),
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_driver_license(self):
        username = "test"
        password = "123"
        license_number = "POE12131"
        driver = Driver.objects.create_user(
            username=username, password=password, license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
