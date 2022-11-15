from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Cook, DishType, Dish


class ModelTests(TestCase):
    def test_driver_str(self):
        driver = Cook.objects.create(
            username="testdriver",
            first_name="firsttest",
            last_name="lasttest",
            license_number="AAA12345"
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name}"
                         f" {driver.last_name})")

    def test_manufacturer_str(self):
        manufacturer = DishType.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self):
        manufacturer = DishType.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Dish.objects.create(
            model="Rav4",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license(self):
        username = "testdriver"
        password = "user12345"
        license_number = "AAA12345"
        driver = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )

        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
