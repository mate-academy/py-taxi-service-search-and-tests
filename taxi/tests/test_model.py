from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacture_str(self):
        manufacture = Manufacturer.objects.create(
            name="volvo",
            country="country_test"
        )
        self.assertEqual(
            str(manufacture),
            f"{manufacture.name} {manufacture.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(username="test",
                                                 password="test1234",
                                                 first_name="test_first",
                                                 last_name="test_last")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def setUp(self):
        self.manufacture = Manufacturer.objects.create(name="test")

    def test_car_str(self):
        car = Car.objects.create(model="test", manufacturer=self.manufacture)
        self.assertEqual(str(car), f"{car.model}")

    def test_creat_driver_with_license_number(self):
        username = "test"
        password = "test1234"
        first_name = "test_first"
        last_name = "test_last"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
