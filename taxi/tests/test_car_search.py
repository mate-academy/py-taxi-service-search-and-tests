from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class CarSearchTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="test12345"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )

        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )

        self.car3 = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer2
        )

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Coroll"}
        )

        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]

        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Corolla")

    def test_search_empty_query_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"))

        cars = response.context["car_list"]

        self.assertEqual(len(cars), 3)

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Unknown"}
        )

        cars = response.context["car_list"]

        self.assertEqual(len(cars), 0)

    def test_search_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "corolla"}
        )

        cars = response.context["car_list"]

        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Corolla")

    def test_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Cor"}
        )

        cars = response.context["car_list"]

        self.assertTrue(
            all("cor" in car.model.lower() for car in cars)
        )

    def test_car_list_view_status_code(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()

        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 302)
