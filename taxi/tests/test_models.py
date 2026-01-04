from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Name",
            country="Country"
        )
        username = "test_username"
        password = "test_password"
        license_number = "test_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        model = "test_model"
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(pk=1)
        self.assertEqual(str(manufacturer), "Name Country")

    def test_driver_str(self):
        driver = get_user_model().objects.get(pk=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.get(pk=1)
        self.assertEqual(str(car), car.model)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(pk=1)
        self.assertEqual("/drivers/1/", driver.get_absolute_url())
