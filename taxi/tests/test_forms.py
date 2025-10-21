from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Manufacturer, Car, Driver


class FormTests(TestCase):
    def test_search(self):
        form_data = {
            "query": "Renault",
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchIntegrationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.manufacturer_ford = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.manufacturer_renault = Manufacturer.objects.create(
            name="Renault",
            country="France"
        )
        self.manufacturer_toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car_focus = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer_ford
        )
        self.car_clio = Car.objects.create(
            model="Clio",
            manufacturer=self.manufacturer_renault
        )
        self.car_corolla = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer_toyota
        )

        self.driver_john = get_user_model().objects.create_user(
            username="john_doe",
            email="john@example.com",
            license_number="DEF67890",
            first_name="John",
            last_name="Doe"
        )
        self.driver_jane = get_user_model().objects.create_user(
            username="jane_smith",
            email="jane@example.com",
            license_number="GHI11111",
            first_name="Jane",
            last_name="Smith"
        )

    def test_manufacturer_search_matching(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"query": "Ford"})

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturer_list), 1)
        self.assertIn(self.manufacturer_ford, manufacturer_list)
        self.assertNotIn(self.manufacturer_renault, manufacturer_list)
        self.assertNotIn(self.manufacturer_toyota, manufacturer_list)

    def test_manufacturer_search_no_matches(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"query": "BMW"})

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturer_list), 0)

    def test_manufacturer_search_case_insensitive(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"query": "renault"})

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturer_list), 1)
        self.assertIn(self.manufacturer_renault, manufacturer_list)

    def test_car_search_matching(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"query": "Focus"})

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]

        self.assertEqual(len(car_list), 1)
        self.assertIn(self.car_focus, car_list)
        self.assertNotIn(self.car_clio, car_list)
        self.assertNotIn(self.car_corolla, car_list)

    def test_car_search_partial_match(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"query": "Cl"})

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]

        self.assertEqual(len(car_list), 1)
        self.assertIn(self.car_clio, car_list)

    def test_car_search_no_matches(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"query": "BMW"})

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]

        self.assertEqual(len(car_list), 0)

    def test_driver_search_matching(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"query": "john"})

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]

        self.assertEqual(len(driver_list), 1)
        self.assertIn(self.driver_john, driver_list)
        self.assertNotIn(self.driver_jane, driver_list)

    def test_driver_search_partial_match(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"query": "jane"})

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]

        self.assertEqual(len(driver_list), 1)
        self.assertIn(self.driver_jane, driver_list)

    def test_driver_search_no_matches(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"query": "bob"})

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]

        self.assertEqual(len(driver_list), 0)

    def test_search_with_empty_query(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"query": ""})

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturer_list), 3)
        self.assertIn(self.manufacturer_ford, manufacturer_list)
        self.assertIn(self.manufacturer_renault, manufacturer_list)
        self.assertIn(self.manufacturer_toyota, manufacturer_list)

    def test_search_without_query_parameter(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]

        self.assertEqual(len(car_list), 3)
        self.assertIn(self.car_focus, car_list)
        self.assertIn(self.car_clio, car_list)
        self.assertIn(self.car_corolla, car_list)

    def test_search_form_in_context(self):
        """Тест, що форма пошуку присутня в контексті"""
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"query": "Ford"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], SearchForm)
        self.assertEqual(response.context["search_form"].initial["query"],
                         "Ford")
