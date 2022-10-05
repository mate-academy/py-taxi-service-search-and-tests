from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelManufacturerTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Country test"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class ModelDriverTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test First",
            last_name="Test Last",
            license_number="ADM56984"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.username, "test")
        self.assertTrue(driver.check_password("test12345"))
        self.assertEqual(driver.license_number, "ADM56984")

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), '/drivers/1/')


class ModelCarTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        car = Car.objects.create(model="test model", manufacturer=manufacturer)

        self.assertEqual(
            str(car),
            f"model: {car.model}; manufacturer: {car.manufacturer.name}"
        )
