from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ManufacturerSearchTestCase(TestCase):
    def setUp(self):
        self.m1 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.m2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "audi"})
        self.assertIn(self.m1, response.context["manufacturer_list"])
        self.assertNotIn(self.m2, response.context["manufacturer_list"])

    def test_empty_search_manufacturer(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": ""})
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            Manufacturer.objects.count(),
        )

    def test_get_manufacturer_search_status_code(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CarSearchTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

        manu = Manufacturer.objects.create(
            name="Volvo",
            country="Sweden"
        )
        self.c1 = Car.objects.create(
            manufacturer=manu,
            model="S80"
        )

    def test_search_car_by_name(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "s80"})
        self.assertIn(self.c1, response.context["car_list"])

    def test_empty_search_car(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": ""})
        self.assertEqual(
            len(response.context["car_list"]),
            Car.objects.count(),
        )


class DriverSearchTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "test"}
        )
        self.assertIn(self.user, response.context["driver_list"])

    def test_empty_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": ""}
        )
        self.assertEqual(
            len(response.context["driver_list"]),
            Driver.objects.count(),
        )
