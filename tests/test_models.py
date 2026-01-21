from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="US")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name}"
                         f" {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            email="<EMAIL>",
            password="<PASSWORD>",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name}"
                         f" {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="US")
        car = Car(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license(self):
        username = "test"
        password = "1234pass"
        license_number = "ASD12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
