from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car_ = Car.objects.create(
            model="Supra",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car_), car_.model)

    def test_driver_str(self):
        driver_ = get_user_model().objects.create_user(
            username="Driver_Test",
            password="Password_Test",
            first_name="First nametest",
            last_name="Last nametest"
        )
        self.assertEqual(
            str(driver_),
            f"{driver_.username} ({driver_.first_name} {driver_.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer_),
            f"{manufacturer_.name} {manufacturer_.country}"
        )

    def test_create_driver_with_license(self):
        username = "Driver_Test"
        password = "Password_Test"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
