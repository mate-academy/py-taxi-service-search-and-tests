from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            first_name="John",
            last_name="Smith",
            license_number="ABC12345",
        )

        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "Toyota Japan",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "john (John Smith)",
        )

    def test_car_str(self):
        self.assertEqual(
            str(self.car),
            "Corolla",
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )
