from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTESTS(TestCase):
    def test_manufacturer_str(self):
        test_manufacturer = Manufacturer.objects.create(
            name="test", country="Test")
        self.assertEqual(str(
            test_manufacturer),
            f"{test_manufacturer.name}, "
            f"{test_manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(username="test",
                                                      password="test1234",
                                                      first_name="test",
                                                      last_name="test",
                                                      license_number="test",)
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} "
                         f"{driver.last_name})")

    def test_create_driver_with_licence(self):
        test_driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="test",
            last_name="test",
            license_number="test",
        )

        self.assertTrue(test_driver)
        self.assertTrue(test_driver.check_password("test1234"))

    def test_car_str(self):
        test_manufacturer = Manufacturer.objects.create(
            name="test", country="Test"
        )
        test_car = Car.objects.create(
            model="test", manufacturer=test_manufacturer
        )

        self.assertEqual(str(test_car), f"{test_car.model}")
