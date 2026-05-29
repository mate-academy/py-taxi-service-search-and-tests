from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Car, Manufacturer, Driver

User = get_user_model()


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alex",
            password="12345"
        )
        self.client.login(username="alex", password="12345")

        self.driver1 = Driver.objects.create_user(
            username="alex",
            password="12345",
            first_name="Alex",
            last_name="Smith"
        )
        self.driver2 = Driver.objects.create_user(
            username="john",
            password="12345",
            first_name="John",
            last_name="Doe"
        )

    def test_driver_search_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"), {"q": "alex"})
        self.assertContains(response, "alex")
        self.assertNotContains(response, "john")

    def test_driver_search_by_first_name(self):
        response = self.client.get(reverse("taxi:driver-list"), {"q": "John"})
        self.assertContains(response, "John")
        self.assertNotContains(response, "alex")

    def test_driver_search_empty(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "alex")
        self.assertContains(response, "john")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alex",
            password="12345"
        )
        self.client.login(username="alex", password="12345")

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car1 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_car_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"q": "X5"})
        self.assertContains(response, "X5")
        self.assertNotContains(response, "Corolla")

    def test_car_search_by_manufacturer(self):
        response = self.client.get(reverse("taxi:car-list"), {"q": "BMW"})
        self.assertContains(response, "X5")
        self.assertNotContains(response, "Corolla")

    def test_car_search_empty(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "X5")
        self.assertContains(response, "Corolla")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alex",
            password="12345"
        )
        self.client.login(username="alex", password="12345")

        self.m1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.m2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"q": "BMW"}
        )
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_manufacturer_search_by_country(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"q": "Japan"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_manufacturer_search_empty(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "BMW")
        self.assertContains(response, "Toyota")
