from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )


class DriverModelTest(TestCase):
    USERNAME = "test_username"
    PASSWORD = "test1234"
    FIRST_NAME = "test_first"
    LAST_NAME = "test_last"
    LICENSE_NUMBER = "ABC12345"

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            license_number=self.LICENSE_NUMBER,
        )

    def test_str(self):

        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_create_with_license_number(self):
        self.assertEqual(self.driver.license_number, self.LICENSE_NUMBER)
        self.assertTrue(self.driver.check_password(self.PASSWORD))
        self.assertEqual(self.driver.username, self.USERNAME)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.pk}/"
        )


class CarModelTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(name="test")
        driver = get_user_model().objects.create(
            username="test",
            password="test1234",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.car.drivers.add(driver)

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
