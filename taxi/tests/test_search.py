from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class DriverSearchTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="john_driver",
            password="pass123",
            license_number="DRV00001",
            first_name="John",
            last_name="Doe"
        )
        get_user_model().objects.create_user(
            username="jane_driver",
            password="pass123",
            license_number="DRV00002",
            first_name="Jane",
            last_name="Smith"
        )
        get_user_model().objects.create_user(
            username="bob_pilot",
            password="pass123",
            license_number="DRV00003",
            first_name="Bob",
            last_name="Johnson"
        )

    def test_search_driver_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "driver"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 2)

        usernames = [driver.username for driver in response.context["driver_list"]]
        self.assertIn("john_driver", usernames)
        self.assertIn("jane_driver", usernames)
        self.assertNotIn("bob_pilot", usernames)

    def test_search_driver_case_insensitive(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "JOHN"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(response.context["driver_list"][0].username, "john_driver")

    def test_search_driver_partial_match(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "jan"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(response.context["driver_list"][0].username, "jane_driver")

    def test_search_driver_no_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "nonexistent"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)

    def test_search_driver_empty_query(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 4)  # Including testuser


class CarSearchTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        tesla = Manufacturer.objects.create(name="Tesla", country="USA")
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")

        Car.objects.create(model="Model 3", manufacturer=tesla)
        Car.objects.create(model="Model S", manufacturer=tesla)
        Car.objects.create(model="X5", manufacturer=bmw)
        Car.objects.create(model="3 Series", manufacturer=bmw)

    def test_search_car_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Model"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)

        models = [car.model for car in response.context["car_list"]]
        self.assertIn("Model 3", models)
        self.assertIn("Model S", models)

    def test_search_car_case_insensitive(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "model 3"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0].model, "Model 3")

    def test_search_car_partial_match(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "X"})

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.context["car_list"]), 1)

    def test_search_car_no_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Nonexistent Model"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_search_car_empty_query(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 4)


class ManufacturerSearchTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Mercedes-Benz", country="Germany")

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "T"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

        names = [m.name for m in response.context["manufacturer_list"]]
        self.assertIn("Tesla", names)
        self.assertIn("Toyota", names)

    def test_search_manufacturer_case_insensitive(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "tesla"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(response.context["manufacturer_list"][0].name, "Tesla")

    def test_search_manufacturer_partial_match(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Benz"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            "Mercedes-Benz"
        )

    def test_search_manufacturer_no_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Nonexistent"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_search_manufacturer_empty_query(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 4)


class SearchPaginationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        for i in range(15):
            get_user_model().objects.create_user(
                username=f"driver{i}",
                password="pass123",
                license_number=f"DRV{i:05d}"
            )

    def test_search_preserves_pagination(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "driver"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
