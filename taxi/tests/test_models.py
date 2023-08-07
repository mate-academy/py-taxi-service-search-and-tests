from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test name", country="test country")
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="username",
            password="test1234",
            first_name="first",
            last_name="last"
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_create_driver_with_valid_license(self):
        username = "username"
        password = "test1234"
        license_number = "ASD12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_model_str(self):
        manufacturer = Manufacturer.objects.create(name="test name")
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
