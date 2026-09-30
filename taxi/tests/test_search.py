from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class TestSearch(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testpass123",
            license_number="QWE12345",
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testpass123",
            license_number="QWE12346",
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany",
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car1 = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer3,
        )
        self.car1.drivers.add(self.user1)

        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1,
        )
        self.car2.drivers.add(self.user1, self.user2)

    def test_search_manufacturer(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )
        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(manufacturers.count(), 1)
        self.assertEqual(manufacturers[0], self.manufacturer1)

    def test_search_car(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "M5"},
        )

        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]

        self.assertEqual(cars.count(), 1)
        self.assertEqual(cars[0], self.car1)

    def test_search_driver(self):
        self.client.force_login(self.user2)

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "testuser1"},
        )

        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]

        self.assertEqual(drivers.count(), 1)
        self.assertEqual(drivers[0], self.user1)
