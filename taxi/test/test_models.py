from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="TestName", country="TestCountry")
        get_user_model().objects.create_user(
            username="TestUsername",
            password="TestPassword",
            first_name="TestFirstName",
            last_name="TestLastName"
        )
        car = Car.objects.create(
            model="TestModel",
            manufacturer=Manufacturer.objects.get(id=1)
        )
        car.drivers.add(get_user_model().objects.get(id=1))

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)
