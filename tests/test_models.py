from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestManufacturerModel(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Porsche",
            country="Germany",
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class TestDriverModel(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="password",
            first_name="first_name",
            last_name="last_name",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="password",
            first_name="first_name",
            last_name="last_name",
        )

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )


class TestCarModel(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Porsche", country="Germany"
        )
        car = Car.objects.create(
            manufacturer=manufacturer,
            model="911",
        )

        self.assertEqual(str(car), f"{car.model}")
