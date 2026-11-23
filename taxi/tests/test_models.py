from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

User = get_user_model()


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            car.model
        )


class DriverModelTests(TestCase):
    USERNAME = "test"
    PASSWORD = "test123"
    LICENSE_NUMBER = "ABC12345"

    def test_driver_str(self):
        driver = User.objects.create(
            username=self.USERNAME,
            password=self.PASSWORD,
            first_name="test_first",
            last_name="test_last"

        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        driver = User.objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD,
            license_number=self.LICENSE_NUMBER
        )
        self.assertEqual(driver.username, self.USERNAME)
        self.assertEqual(driver.license_number, self.LICENSE_NUMBER)
        self.assertTrue(driver.check_password(self.PASSWORD))

    def test_driver_get_absolute_url(self):
        driver = User.objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD,
            license_number=self.LICENSE_NUMBER
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )
