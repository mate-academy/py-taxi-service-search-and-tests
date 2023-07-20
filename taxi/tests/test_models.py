from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "testusername"
        cls.password = "123testadmin"
        cls.license_number = "AAA11111"

        cls.manufacturer = Manufacturer.objects.create(
            name="manufacturer-test",
            country="country-test"
        )
        cls.driver = get_user_model().objects.create_user(
            username="testusername",
            first_name="First name Test",
            last_name="Last name Test",
            password="123testadmin",
            license_number="AAA11111"
        )

    def test_manufacturer_str(self):
        str_name = f"{self.manufacturer.name} {self.manufacturer.country}"
        self.assertEqual(str(self.manufacturer), str_name)

    def test_driver_str(self):
        str_name = (f"{self.driver.username} "
                    f"({self.driver.first_name} {self.driver.last_name})")
        self.assertEqual(str(self.driver), str_name)

    def test_car_str(self):
        car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )
        car.drivers.add(self.driver)

        self.assertEqual(str(car), car.model)

    def test_create_driver_license_number(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertTrue(self.driver.check_password(self.password))
        self.assertEqual(
            self.driver.license_number,
            self.license_number
        )

    def test_get_driver_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            "/drivers/1/"
        )
