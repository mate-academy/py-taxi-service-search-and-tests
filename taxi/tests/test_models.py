from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="usa"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        username = "test"
        password = "11111111"
        first_name = "first"
        last_name = "last"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(
            str(driver), f"{username} ({first_name} {last_name})"
        )

    def test_driver_get_absolute_url(self):
        username = "test"
        password = "11111111"
        first_name = "first"
        last_name = "last"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="usa"
        )
        car = Car.objects.create(
            model="bmw",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)
