from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class DriverTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(10):
            Driver.objects.create(
                username=f"driver_number_{i}",
                license_number=f"license_number_{i}"
            )

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin", password="hard", email="anton@gmail.com"
        )
        self.client.force_login(self.admin_user)

    def test_connection(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_pagination_second_page(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_search_form_one_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "driver_number_1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("driver_list" in response.context)
        self.assertTrue(len(response.context["driver_list"]), 1)
        self.assertTrue(
            response.context["driver_list"][0].username == "driver_number_1"
        )

    def test_search_form_zero_results(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "nothing"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("driver_list" in response.context)
        self.assertEqual(len(response.context["driver_list"]), 0)

    def test_search_form_all_results(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("driver_list" in response.context)
        self.assertEqual(len(response.context["driver_list"]), 5)
