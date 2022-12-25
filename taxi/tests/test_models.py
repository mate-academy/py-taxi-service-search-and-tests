from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def test_manufacturer_str(self):
        manufacture = Manufacturer.objects.create(name="test_name", country="test_country")

        self.assertEqual(str(manufacture), f"{manufacture.name} {manufacture.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="test first",
            last_name="test last"
        )

        self.assertEqual(str(driver), "test (test first test last)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name", country="test_country")
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)

        self.assertEqual(str(car), "test_model")

    def test_create_driver_with_license(self):
        username = "test user"
        password = "test password"
        license_number = "test license number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
