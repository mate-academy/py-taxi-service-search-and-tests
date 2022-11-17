from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="some_name",
            email="test@noma.il",
            password="123435poi",
            first_name="Le_first_name",
            last_name="Le_second_also_name"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="UA"
        )

        car = Car.objects.create(
            model="Test 001",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "Test 001")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Awesome Inc.",
            country="UA"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_creation(self):
        username = "whywouldyouknow"
        password = "iwont123tellya"
        first_name = "Mark"
        last_name = "Jones"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

        self.assertTrue(driver.check_password(password))
