from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.driver = Driver.objects.create_user(
            username="Test Driver",
            first_name="Test Driver First",
            last_name="Test Driver Last",
            password="test_password_12345",
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
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

    def test_driver_license(self):
        data_dict = {
            "username": "Driver",
            "password": "just_password",
            "license_number": "QWE12345",
        }

        driver = Driver.objects.create_user(**data_dict)
        self.assertEqual(driver.license_number, data_dict["license_number"])
