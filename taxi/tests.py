from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class TaxiViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="alice",
            password="password123",
            license_number="ABC12345",
        )
        cls.second_driver = Driver.objects.create_user(
            username="alicia",
            password="password123",
            license_number="XYZ12345",
        )
        cls.unrelated_driver = Driver.objects.create_user(
            username="bob",
            password="password123",
            license_number="BOB12345",
        )
        cls.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        cls.honda = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        cls.corolla = Car.objects.create(
            model="Corolla",
            manufacturer=cls.toyota,
        )
        cls.camry = Car.objects.create(
            model="Camry",
            manufacturer=cls.toyota,
        )
        cls.civic = Car.objects.create(
            model="Civic",
            manufacturer=cls.honda,
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_index_shows_database_counts_and_visit_number(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 3)
        self.assertEqual(response.context["num_cars"], 3)
        self.assertEqual(response.context["num_manufacturers"], 2)
        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 2)

    def test_driver_list_searches_username_case_insensitively(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "ALIC"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context["driver_list"],
            [self.driver, self.second_driver],
        )

    def test_driver_list_search_can_use_common_search_parameter(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "bob"},
        )

        self.assertEqual(
            list(response.context["driver_list"]),
            [self.unrelated_driver],
        )

    def test_car_list_searches_model_case_insensitively(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "ORO"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), [self.corolla])

    def test_manufacturer_list_searches_name_case_insensitively(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [self.toyota],
        )

    def test_blank_search_returns_all_items(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "   "},
        )

        self.assertEqual(response.context["car_list"].count(), 3)

    def test_search_with_no_matches_returns_empty_list(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "no such manufacturer"},
        )

        self.assertEqual(response.context["manufacturer_list"].count(), 0)

    def test_search_is_preserved_across_pages(self):
        for number in range(6):
            Manufacturer.objects.create(
                name=f"Toyota {number}",
                country="Japan",
            )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toyota"},
        )

        self.assertTrue(response.context["is_paginated"])
        self.assertContains(response, b"name=Toyota&page=2")

    def test_list_view_redirects_anonymous_user_to_login(self):
        self.client.logout()

        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_toggle_assign_to_car_adds_and_removes_car(self):
        url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.corolla.pk},
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.driver.cars.filter(pk=self.corolla.pk).exists())

        self.client.get(url)
        self.assertFalse(self.driver.cars.filter(pk=self.corolla.pk).exists())
