from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name="Mercedes",
                                                   country="Ukraine")
        for i in range(10):
            Car.objects.create(model=f"Car_{i}",
                               manufacturer=manufacturer)

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin", password="hard", email="anton@gmail.com"
        )
        self.client.force_login(self.admin_user)

    def test_connection(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination_first_page(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_pagination_second_page(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_search_form_with_one_result(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "Car_0"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("car_list", response.context)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0].model, "Car_0")

    def tes_search_form_with_zero_result(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "Pampam"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("car_list", response.context)
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_search_form_all_results(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("car_list", response.context)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_search_form_all_results_second_page(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "", "page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertIn("car_list", response.context)
        self.assertEqual(len(response.context["car_list"]), 5)
        (self.assertTrue
         ("Car_5" == response.context["car_list"][0].model))
