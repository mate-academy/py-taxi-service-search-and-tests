from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="manufacturer_test",
            country="country_test"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="manufacturer_test",
            country="country_test"
        )

        car = Car.objects.create(
            model="model_test",
            manufacturer=manufacturer
        )

        self.assertEqual(
            str(car),
            car.model
        )

    def test_driver(self):
        username = "test_username"
        password = "test12345"
        first_name = "test first"
        last_name = "test last"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

        self.assertTrue(driver.check_password(password))
