from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.driver = Driver.objects.create(
            username="testdriver",
            first_name="Test",
            last_name="Driver",
            license_number="123456",
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "Test Manufacturer Test Country"
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "testdriver (Test Driver)")

    def test_car_str(self):
        self.assertEqual(str(self.car), "Test Car")

    def test_driver_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)

    def test_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)
