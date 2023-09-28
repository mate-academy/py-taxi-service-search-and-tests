from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):
    def test_str_representation(self):
        manufacturer = Manufacturer(name="Toyota", country="Japan")
        self.assertEqual(str(manufacturer), "Toyota Japan")


class CarModelTest(TestCase):
    def test_str_representation(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Camry")


class DriverModelTest(TestCase):
    def test_str_representation(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver), "test_user (John Doe)")

    def test_create_driver_with_license(self):
        password = "1qazcde3"
        driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
            password=password
        )
        self.assertEqual(driver.username, "test_user")
        self.assertEqual(driver.first_name, "John")
        self.assertEqual(driver.last_name, "Doe")
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertTrue(driver.check_password(password))

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
            password="1qazcde3"
        )
        driver.save()
        url = driver.get_absolute_url()
        self.assertEqual(url, f"/drivers/{driver.pk}/")
