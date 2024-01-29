from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test_country",)
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create(username="test_user", first_name="test_first", last_name="test_last")
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test_country")
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):  #change name func
        username = "test_user"
        password = "test123"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
        # self.assertEqual(
        #     driver.get_absolute_url(), "/drivers/1/"
        # )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="test_first",
            last_name="test_last"
        )
        self.assertEqual(
            driver.get_absolute_url(), "/drivers/1/"
        )
