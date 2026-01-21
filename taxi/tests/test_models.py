from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        driver = get_user_model().objects.create_user(
            username="test_user",
            email="test@test.com",
            password="test1234",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        car.drivers.add(driver)

    def test_driver_str_method(self):
        driver = get_user_model().objects.get(username="test_user")
        return self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.get(username="test_user")
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")

    def test_create_driver_with_license_number(self):
        license_number = ("TST00000",)
        password = "test_password_2"
        driver = get_user_model().objects.get(username="test_user")
        driver.license_number = license_number
        driver.set_password(password)

        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_manufacturer_str_method(self):
        manufacturer = Manufacturer.objects.get(name="test_manufacturer")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str_method(self):
        car = Car.objects.get(model="test_model")
        self.assertEqual(str(car), car.model)
