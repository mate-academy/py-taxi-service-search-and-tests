from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="FCA",
            country="Italy"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="testpassword",
            first_name="first_test",
            last_name="last_test"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        user = get_user_model().objects.create(
            username="test",
            password="testpassword",
            first_name="first_test",
            last_name="last_test"
        )
        driver = get_user_model().objects.get(id=user.id)
        self.assertEqual(
            driver.get_absolute_url(),
            f"/drivers/{driver.id}/"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "testpassword"
        license_number = "TC000000"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="FCA",
            country="Italy"
        )
        driver1 = get_user_model().objects.create(
            username="test1",
            password="testpassword1",
            first_name="first_test1",
            last_name="last_test1",
            license_number="TC000000"
        )

        driver2 = get_user_model().objects.create(
            username="test2",
            password="testpassword2",
            first_name="first_test2",
            last_name="last_test2",
            license_number="TC000001"
        )

        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        car.drivers.set([driver1, driver2])

        self.assertEqual(str(car), car.model)
