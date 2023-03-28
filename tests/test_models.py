from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Car, Manufacturer


class ModelTest(TestCase):
    def test_model_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_model_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        car = Car.objects.create(model="TestModel", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_model_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="12345",
            first_name="first_test",
            last_name="last_test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_create_user_with_license(self):
        username = "test"
        password = "12345"
        license_plate = "ASD12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_plate,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_plate)
        self.assertTrue(driver.check_password(password))
