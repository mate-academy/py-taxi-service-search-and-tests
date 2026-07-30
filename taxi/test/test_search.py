from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class SearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin",
            password="password",
            license_number="ABC12345"
        )
        self.client.login(
            username="admin",
            password="password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="michael",
            password="password",
            license_number="XYZ12345"
        )
        self.other_driver = Driver.objects.create_user(
            username="alex",
            password="password",
            license_number="AAA12345"
        )

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"}
        )

        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(
            manufacturers.count(),
            1
        )
        self.assertEqual(
            manufacturers.first(),
            self.manufacturer
        )

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"}
        )

        cars = response.context["car_list"]

        self.assertEqual(
            cars.count(),
            1
        )
        self.assertEqual(
            cars[0],
            self.car
        )

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "mich"}
        )

        drivers = response.context["object_list"]

        self.assertEqual(
            drivers.count(),
            1
        )
        self.assertEqual(
            drivers[0],
            self.driver
        )
