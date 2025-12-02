from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        self.assertEqual(str(manufacturer), "Tesla USA")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="johndoe", first_name="John", last_name="Doe"
        )
        self.assertEqual(str(driver), "johndoe (John Doe)")

    def test_car_str(self):
        car = Car.objects.create(
            model="Model S",
            manufacturer=Manufacturer.objects.create(name="Tesla")
        )
        self.assertEqual(str(car), "Model S")

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            username="johndoe", first_name="John", last_name="Doe"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")

    def test_create_driver_with_license(self):
        username = "johndoe"
        first_name = "John"
        last_name = "Doe"
        license_number = "ABC456789"
        password = "test123"

        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
            password=password,
        )

        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.get_full_name(), f"{first_name} {last_name}")
        self.assertTrue(driver.check_password(password))
