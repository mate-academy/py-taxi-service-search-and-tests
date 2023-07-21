from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEquals(
            str(manufacturer_), f"{manufacturer_.name} {manufacturer_.country}"
        )

    def test_driver_str(self,):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )
        self.assertEquals(
            str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer_
        )
        self.assertEquals(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "Test license"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)
