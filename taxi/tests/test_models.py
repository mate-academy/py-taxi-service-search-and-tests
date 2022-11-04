from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_create_driver_with_license_number(self):
        password = "something123"
        license_number = "ASD12345"

        driver = get_user_model().objects.create_user(
            password=password,
            license_number=license_number,
            username="driver",
            first_name="Jason",
            last_name="Statham"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

        self.assertTrue(driver.check_password(password))

        self.assertEqual(driver.license_number, license_number)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="ZAZ", country="Ukraine"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="ZAZ Lanos",
            manufacturer=Manufacturer.objects.create(
                name="ZAZ", country="Ukraine"
            )
        )

        self.assertEqual(str(car), car.model)
