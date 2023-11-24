from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


# Create your tests here.


class ModelTests(TestCase):
    def test_manufacturer_sts(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="Countrytest")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="test1",
            last_name="test2"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_create_with_license_number(self):
        username = "test"
        password = "testpas123"
        license_number = "AAA33333"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_get_driver_absolute_url(self):
        username = "test"
        password = "testpas123"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        absolute_url = driver.get_absolute_url()
        self.assertEqual(absolute_url, f"/drivers/{driver.id}/")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="Countrytest")
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
