from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="admin1",
            password="admin123451",
            first_name="Keanu",
            last_name="Reeves",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mercedes-Bens", country="Germany"
        )
        car = Car.objects.create(model="AMG", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "admin1"
        password = "admin123452"
        license_number = "AD25467"
        driver = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="admin1",
            password="admin123451",
        )
        expected_url = f"/drivers/{driver.pk}/"

        self.assertEqual(driver.get_absolute_url(), expected_url)
