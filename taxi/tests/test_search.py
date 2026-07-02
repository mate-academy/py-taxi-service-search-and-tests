from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="John",
            password="12345",
            license_number="QWE12345"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Mercedes", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_search_manufacturer_list(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"}
        )
        manufacturer = res.context["manufacturer_list"]
        self.assertEqual(len(manufacturer), 1)
        self.assertEqual(manufacturer[0].name, "Toyota")


class CarViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="John",
            password="12345",
            license_number="QWE12345"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="M3", manufacturer=manufacturer)
        Car.objects.create(model="Hybrid", manufacturer=manufacturer)

    def test_search_car_by_model(self):
        res = self.client.get(
            reverse("taxi:car-list"),
            {"model": "hy"}
        )
        cars = res.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Hybrid")


class DriverViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="John",
            password="12345",
            license_number="QWE12345"
        )
        Driver.objects.create_user(
            username="Den",
            password="12345",
            license_number="AXS78781"
        )
        Driver.objects.create_user(
            username="Anna",
            password="12345",
            license_number="BBB83471"
        )
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        res = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "D"}
        )
        drivers = res.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "Den")
