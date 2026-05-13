from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="test")
        self.username = "test"
        self.password = "test123"
        self.first_name = "test"
        self.last_name = "test"
        self.license_number = "ORU152635"
        self.driver = Driver.objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            license_number=self.license_number)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})")
        self.assertEqual(self.driver.license_number, self.license_number)
        self.assertTrue(self.driver.check_password(self.password))

    def test_car_str(self):
        car = Car.objects.create(model="test", manufacturer=self.manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")
