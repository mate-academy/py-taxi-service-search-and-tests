from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(name="Toyota", country="Japan")
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_car_str(self):
        car = Car(model="Corolla")
        self.assertEqual(str(car), "Corolla")

    def test_driver_str(self):
        driver = get_user_model()(
            username="john", first_name="John", last_name="Doe"
        )
        self.assertEqual(str(driver), "john (John Doe)")

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="driver", password="test12345", license_number="ABC12345"
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", args=[driver.pk]),
        )
