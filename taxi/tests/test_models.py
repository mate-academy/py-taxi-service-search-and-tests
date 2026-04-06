from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test_Driver",
            password="test123",
            first_name="Test_First",
            last_name="Test_Last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            username="Test_Driver",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.id})
        )


class CarModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        car = Car.objects.create(
            model="Test_Car",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
