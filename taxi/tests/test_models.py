from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def create_manufacturer(self):
        return Manufacturer.objects.create(name="test", country="text country")

    def create_driver(self):
        username = "test_username"
        password = "test12345"
        first_name = "test_first_name"
        last_name = "test_last_name"
        license_number = "test_license"
        return get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )

    def create_car(self, manufacturer, driver):
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        return car

    def test_manufacturer_str(self):
        manufacturer = self.create_manufacturer()
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = self.create_driver()
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = self.create_manufacturer()
        driver = self.create_driver()
        car = self.create_car(manufacturer, driver)
        self.assertEqual(str(car), car.model)

    def test_create_licence_number(self):
        driver = self.create_driver()
        self.assertEqual(driver.username, "test_username")
        self.assertTrue(driver.check_password("test12345"))
        self.assertEqual(driver.first_name, "test_first_name")
        self.assertEqual(driver.last_name, "test_last_name")
        self.assertEqual(driver.license_number, "test_license")
