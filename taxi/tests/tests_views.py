from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class ViewTest(TestCase):

    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin",
            password="password123",
            license_number="ADMIN123"
        )

    def test_pages_return_200(self):
        self.client.login(
            username="admin",
            password="password123"
        )

        urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list"),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_pages_require_login(self):
        urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list"),
        ]

        for url in urls:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 302)

    def test_driver_pagination(self):
        self.client.login(
            username="admin",
            password="password123"
        )

        for i in range(10):
            Driver.objects.create_user(
                username=f"driver{i}",
                password="password123",
                license_number=f"ABC{i}"
            )

        response = self.client.get(
            reverse("taxi:driver-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            len(response.context["driver_list"]),
            5
        )

    def test_car_pagination(self):
        self.client.login(
            username="admin",
            password="password123"
        )

        manufacturer = Manufacturer.objects.create(
            name="Rover",
            country="UK"
        )

        for i in range(10):
            Car.objects.create(
                model=f"Car {i}",
                manufacturer=manufacturer
            )

        response = self.client.get(
            reverse("taxi:car-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            len(response.context["object_list"]),
            5
        )

    def test_manufacturer_pagination(self):
        self.client.login(
            username="admin",
            password="password123"
        )

        for i in range(10):
            Manufacturer.objects.create(
                name=f"Manufacturer {i}",
                country="UK"
            )

        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            5
        )
