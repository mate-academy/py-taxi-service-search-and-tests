from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        username = "test_user"
        password = "password1234"
        first_name = "test_first"
        last_name = "test_last"
        license_number = "test_number"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )

        self.assertEqual(str(driver),
                         f"{driver.username} ({driver.first_name}"
                         f" {driver.last_name})")
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.get_absolute_url())

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,

        )

        self.assertEqual(str(car), car.model)
