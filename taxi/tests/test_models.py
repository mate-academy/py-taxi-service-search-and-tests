from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="USA",
        )
        self.driver = get_user_model().objects.create(
            username="driver",
            license_number="AAA11111",
            password="Password!",
            first_name="first name",
            last_name="last name",
        )

    def test_manufacturer_str(self):
        manufacturer = self.manufacturer
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        driver = self.driver
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Model",
            manufacturer=self.manufacturer,
        )

        self.assertEqual(str(car), car.model)
