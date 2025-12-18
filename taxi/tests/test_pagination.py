from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car

User = get_user_model()


class PaginationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user1",
            password="pass123",
            license_number="AAA11111"
        )

        for i in range(12):
            manufacturer = Manufacturer.objects.create(
                name=f"Manufacturer {i}",
                country="Country"
            )
            Car.objects.create(
                model=f"CarModel {i}",
                manufacturer=manufacturer
            )
            User.objects.create_user(
                username=f"driver{i}",
                password="pass123",
                license_number=f"LIC{i:05d}"
            )

    def setUp(self):
        self.client = Client()
        self.client.login(username="user1", password="pass123")

    def test_manufacturer_pagination(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

        response2 = self.client.get(url, {"page": 2})
        self.assertEqual(len(response2.context["manufacturer_list"]), 5)

        response3 = self.client.get(url, {"page": 3})
        self.assertEqual(len(response3.context["manufacturer_list"]), 2)

    def test_car_pagination(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

        response2 = self.client.get(url, {"page": 3})
        self.assertEqual(len(response2.context["car_list"]), 2)

    def test_driver_pagination(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

        response2 = self.client.get(url, {"page": 3})
        self.assertEqual(len(response2.context["driver_list"]), 3)
