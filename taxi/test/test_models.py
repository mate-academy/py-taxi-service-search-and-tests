from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.driver = Driver.objects.create_user(
            username="john",
            password="password",
            first_name="John",
            last_name="Smith",
            license_number="ABC12345"
        )

        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "BMW Germany"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "john (John Smith)"
        )

    def test_car_str(self):
        self.assertEqual(
            str(self.car),
            "X5"
        )

    def test_driver_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.driver.pk}
            )
        )
