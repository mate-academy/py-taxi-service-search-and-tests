from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car
from taxi.forms import SearchForm


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )
        Driver.objects.create_user(
            username="alex",
            password="test12345",
            license_number="XYZ54321",
        )

        manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )

        Car.objects.create(
            model="X5",
            manufacturer=manufacturer1,
        )
        Car.objects.create(
            model="Model S",
            manufacturer=manufacturer2,
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "jo"},
        )

        self.assertContains(response, "john")
        self.assertNotContains(response, "alex")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "X5"},
        )

        self.assertContains(response, "X5")
        self.assertNotContains(response, "Model S")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "BMW"},
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Tesla")

    def test_search_form_empty_query_is_valid(self):
        form = SearchForm(data={"query": ""})

        self.assertTrue(form.is_valid())

    def test_search_form_query_is_valid(self):
        form = SearchForm(data={"query": "BMW"})

        self.assertTrue(form.is_valid())

    def test_search_form_in_driver_context(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertIn("search_form", response.context)

    def test_search_form_in_car_context(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertIn("search_form", response.context)

    def test_search_form_in_manufacturer_context(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertIn("search_form", response.context)

    def test_empty_driver_query_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertContains(response, "john")
        self.assertContains(response, "alex")

    def test_empty_car_query_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertContains(response, "X5")
        self.assertContains(response, "Model S")

    def test_empty_manufacturer_query_returns_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertContains(response, "BMW")
        self.assertContains(response, "Tesla")
