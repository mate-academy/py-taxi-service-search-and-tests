from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_model_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test manufacturer country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_model_str_method(self):
        driver = Driver.objects.create_user(
            username="Test Driver",
            password="Test Password",
            first_name="Test First",
            last_name="Test Last",
            email="mail@example.com",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_model_get_absolute_url_func(self):
        driver = Driver.objects.create_user(
            username="Test Driver",
            password="Test Password",
            first_name="Test First",
            last_name="Test Last",
            email="mail@example.com",
        )
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": driver.id}
        )
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_car_model_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test manufacturer country",
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
