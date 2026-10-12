from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    LICENSE_NUMBER = "ABC12345"
    USERNAME = "test"
    PASSWORD = "test1234"
    FIRST_NAME = "test_first_name"
    LAST_NAME = "test_last_name"

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            license_number=self.LICENSE_NUMBER,
            username=self.USERNAME,
            password=self.PASSWORD,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            car.model
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            license_number=self.LICENSE_NUMBER,
            username=self.USERNAME,
            password=self.PASSWORD,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
        )
        self.assertEqual(driver.license_number, self.LICENSE_NUMBER)
        self.assertEqual(driver.username, self.USERNAME)
        self.assertTrue(driver.check_password(self.PASSWORD))
        self.assertEqual(driver.first_name, self.FIRST_NAME)
        self.assertEqual(driver.last_name, self.LAST_NAME)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            license_number=self.LICENSE_NUMBER,
            username=self.USERNAME,
            password=self.PASSWORD,
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )
