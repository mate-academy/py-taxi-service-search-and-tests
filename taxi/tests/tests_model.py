from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="test"
        )
        self.driver = Driver.objects.create(
            username="User test",
            first_name="First_test",
            last_name="Last_test",
            license_number="123456",
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "test test"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "User test (First_test Last_test)"
        )

    def test_driver_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)

    def test_car_str(self):
        self.assertEqual(str(self.car), "Test Car")

    def test_driver_with_license_number(self):
        username = "test_username"
        password = "test1234"
        license_number = "AAA54321"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)
