from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestManufacturerModel(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )


class TestDriverModel(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="test_user",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver),
                         f"{self.driver.username} "
                         f"({self.driver.first_name} {self.driver.last_name})")

    def test_driver_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(),
                         f"/drivers/{self.driver.id}/")

    def test_driver_with_licence_number(self):
        username = "test_user1"
        password = self.driver.password
        first_name = self.driver.first_name
        last_name = self.driver.last_name
        license_number = "AAA11111"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.check_password(password), True)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)


class TestCarModel(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        self.car = Car.objects.create(model="test_model",
                                      manufacturer=self.manufacturer, )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
