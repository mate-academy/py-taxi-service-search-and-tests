from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test country"
        )
        driver = get_user_model().objects.create_user(
            username="test",
            password="123",
            first_name="testfirst",
            last_name="testlast",
        )
        car = Car.objects.create(
            model="testmodel",
            manufacturer=manufacturer
        )
        car.drivers.set([driver])

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_meta_ordering(self):
        self.assertListEqual(
            Manufacturer._meta.ordering,
            ["name"]
        )

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolut_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            driver.get_absolute_url(),
            "/drivers/1/"
        )

    def test_create_driver_license_number(self):
        driver = Driver.objects.get(id=1)
        driver.license_number = "SDF12345"
        self.assertEqual(
            driver.license_number,
            "SDF12345"
        )

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(
            str(car),
            f"{car.model}"
        )
