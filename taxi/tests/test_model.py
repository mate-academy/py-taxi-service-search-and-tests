from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="driver",
            password="password1234",
            first_name="driverD",
            last_name="driverL"
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} "
                         f"{driver.last_name})")

    def test_car_str(self):
        car = Car("car")
        self.assertEqual(str(car), car.model)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test96859",
        )

        absolute_url = driver.get_absolute_url()

        self.assertEquals(absolute_url, f"/drivers/{driver.id}/")

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "pas123456"
        license_number = "QWE12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)
