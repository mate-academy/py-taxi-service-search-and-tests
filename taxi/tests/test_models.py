from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="testuser",
            password="testpassword",
            first_name="Test_first",
            last_name="test_last",
            license_number="123456",
        )
        expected_str = f"{driver.username} ({driver.first_name} {driver.last_name})"
        self.assertEqual(str(driver), expected_str)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        car = Car.objects.create(model="Test Model", manufacturer=manufacturer)
        expected_str = "Test Model"
        self.assertEqual(str(car), expected_str)

    def test_create_driver(self):
        username = "testuser"
        password = "testpassword"
        license_number = "123456"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="Test_first",
            last_name="test_last",
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_get_absolute_url(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test_first",
            last_name="test_last",
            license_number="123456",
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": self.driver.id})
        actual_url = self.driver.get_absolute_url()
        self.assertEqual(actual_url, expected_url)
