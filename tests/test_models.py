from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver

USERNAME = "test"
PASSWORD = "PASSWORD"
FIRST_NAME = "test_first"
LAST_NAME = "test_last"
LICENSE_NUMBER = "test_license_number"


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create_user(
            username=USERNAME,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            license_number=LICENSE_NUMBER,
            password=PASSWORD,
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="USA")
        self.assertEqual(str(manufacturer), "test USA")

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=self.driver.id)
        self.assertEqual(str(driver), f"{USERNAME} ({FIRST_NAME} {LAST_NAME})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="USA")
        driver = get_user_model().objects.get(id=self.driver.id)
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        car.drivers.set([driver])
        self.assertEqual(str(car), "test")

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=self.driver.id)
        self.assertEqual(driver.username, USERNAME)
        self.assertEqual(driver.license_number, LICENSE_NUMBER)
        self.assertTrue(driver.check_password(PASSWORD))

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=self.driver.id)
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")
