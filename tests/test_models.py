from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="TEST")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "Test License Number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="TEST")
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="12345",
            license_number="123456")

    def test_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.pk})
        actual_url = self.driver.get_absolute_url()
        self.assertEqual(expected_url, actual_url)
