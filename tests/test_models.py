from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.driver = get_user_model().objects.create(
            username="test_username",
            password="test_password",
            first_name="test_First_Name",
            last_name="test_Last_Name",
        )
        self.car = Car.objects.create(
            model="test_model", manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "test_username (test_First_Name test_Last_Name)",
        )

    def test_car_str(self):
        self.car.drivers.add(self.driver)
        self.assertEqual(str(self.car), self.car.model)

    def test_drivers_verbose_names(self):
        self.assertEqual(get_user_model()._meta.verbose_name, "driver")
        self.assertEqual(get_user_model()._meta.verbose_name_plural, "drivers")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", args=[self.driver.pk]),
        )
