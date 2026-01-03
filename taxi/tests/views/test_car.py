import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarListViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="bob",
            password="ccc123"
        )
        self.client.force_login(user)

        mercedes = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        random_car = ["BMW", "Audi", "ZAZ", "MAN", "Scania", "Ford"]
        for i in range(7):
            Car.objects.create(
                model=f"{random.choice(random_car)} №{i}",
                manufacturer=mercedes,
            )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars[:5])
        )
        self.assertTrue("search_form" in response.context)

    def test_pagination_is_5(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_valid_search(self):
        model = "№2"
        response = self.client.get(CAR_LIST_URL + f"?model={model}")
        self.assertEqual(response.status_code, 200)

        expected_car = Car.objects.filter(model__icontains=model)
        self.assertIsNotNone(expected_car)
        self.assertTrue(expected_car.exists())
        self.assertEqual(
            list(response.context["car_list"]),
            list(expected_car)
        )

    def test_search_not_found(self):
        response = self.client.get(CAR_LIST_URL + "?model=invalid}")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["car_list"]), 0)
