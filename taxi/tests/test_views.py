from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import (
    Manufacturer,
    Car,
    Driver
)

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="User",
            password="userpass123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Volkswagen", country="Germany"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Peugeot", country="France"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL, {"name": "Volkswagen"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Volkswagen")
        self.assertNotContains(response, "Toyota Japan")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="User",
            password="userpass123",
        )
        self.client.force_login(self.user)
        Driver.objects.create(username="Michael", license_number="MSA12345")
        Driver.objects.create(username="Kimmi", license_number="KRA12345")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "Michael"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Michael")
        self.assertNotContains(response, "Kimmi")


class PublicCarTest(TestCase):

    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarListViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="User",
            password="userpass123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany"
        )
        Car.objects.create(model="Skoda", manufacturer=manufacturer)
        Car.objects.create(model="Super-B", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
