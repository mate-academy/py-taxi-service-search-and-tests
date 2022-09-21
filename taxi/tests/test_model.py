from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class TestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username="test_drive",
                                             password="test12345",
                                             first_name="Bob",
                                             last_name="Smith",
                                             license_number="AAA12345"
                                             )
        Manufacturer.objects.create(name="Test", country="Country_test")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(str(manufacturer), "Test Country_test")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        driver = get_user_model().objects.get(id=1)
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        car.drivers.add(driver)

        self.assertEqual(str(car), car.model)

    def test_user_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_create_user_with_license(self):
        username = "test_drive2"
        license_number = "BBB6789"
        password = "user123456"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.license_number, license_number)

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
