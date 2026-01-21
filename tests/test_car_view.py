from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CARS_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(CARS_URL)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

        number_of_cars = 10
        for car_id in range(1, number_of_cars):
            Car.objects.create(
                model=f"Model{car_id}",
                manufacturer=Manufacturer.objects.create(
                    name=f"Name{car_id}", country=f"Country{car_id}"
                )
            )

    def test_retrieve_cars(self):
        response = self.client.get(CARS_URL)
        cars = Car.objects.all()[:5]
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_view_uses_correct_template(self):
        response = self.client.get(CARS_URL)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_logged_in_access(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_query_search_filter(self):
        response = self.client.get(f"{CARS_URL}?model=Model1")
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="Model1")
        )
