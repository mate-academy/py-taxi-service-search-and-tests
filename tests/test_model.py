# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taxi_service.settings")
#
# import django
# django.setup()
#

from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test_Virtual_manufacturer", country="Oz"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:

        driver = get_user_model().objects.create(
            username="test",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
        )

        manufacturer_test = Manufacturer.objects.create(
            name="Test_Virtual_Manufacturer", country="Oz"
        )
        car_test = Car.objects.create(
            model="M_Test_X5",
            manufacturer=manufacturer_test,
        )
        car_test.drivers.add(driver)
        self.assertEqual(str(car_test), car_test.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "tets1234"
        license_number = "JIM26571"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
