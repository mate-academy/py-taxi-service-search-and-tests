from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test2",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="te1123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test",
        )
        self.client.force_login(self.user)
        Car.objects.create(
            model="BMW X5",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Grand",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_search_by_model(self):
        response = self.client.get(
            CAR_URL,
            {"model": "Camry"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Grand")
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "BMW X5")

    def test_search_case_insensitive(self):
        response = self.client.get(
            CAR_URL,
            {"model": "bmW x5"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW X5")
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Grand")
        self.assertNotContains(response, "Camry")

    def test_empty_search_returns_all(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": ""}
        )

        self.assertContains(response, "Corolla")
        self.assertContains(response, "Camry")
        self.assertContains(response, "BMW X5")
