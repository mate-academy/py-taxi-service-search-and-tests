from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str_representation(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        expected_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_str)

    def test_driver_str_representation(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_firs",
            last_name="test_last",
        )
        self.assertEqual(str(driver), f"{driver.username}"
                                      f" ({driver.first_name}"
                                      f" {driver.last_name})")

    def test_car_str_representation(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        model = Car.objects.create(
            model="Mustang",
            manufacturer=manufacturer
        )
        self.assertEqual(str(model), f"{model.model}")

    def test_driver_license_number_str_representation(self):
        username = "test"
        password = "test123"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(str(driver.username), username)
        self.assertEqual(str(driver.license_number), license_number)
        self.assertTrue(driver.check_password(password))
