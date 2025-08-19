from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class  ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Manufacturer", country="Country")
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")
        self.assertEqual(str(manufacturer), "Manufacturer Country")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="admin",
            license_number="ADM12346",
            first_name="Name",
            last_name="Surname",
            password="1qazcde3",
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")
        self.assertEqual(str(driver), "admin (Name Surname)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Manufacturer", country="Country")
        car = Car.objects.create(model="Model", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
        self.assertEqual(str(car), "Model")

    def test_driver_license(self):

        license_number = "ADM12346"
        username = "admin"
        password = "1qazcde3"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            first_name="Name",
            last_name="Surname",
            password=password,
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
