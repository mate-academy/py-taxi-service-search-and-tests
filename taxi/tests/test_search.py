from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarListViewSearchTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )
        self.driver = get_user_model().objects.create_user(
            username="test111",
            password="paSS1ord",
            license_number="ABC12345"
        )
        self.car1 = Car.objects.create(
            model="CBR-1000",
            manufacturer=self.manufacturer
        )
        self.car1.drivers.add(self.driver)

        self.car2 = Car.objects.create(
            model="Tesla Model S",
            manufacturer=self.manufacturer
        )
        self.car2.drivers.add(self.driver)
        self.client.login(username="test111", password="paSS1ord")

    def test_search_car_by_exact_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Tesla Model S"}
        )
        self.assertContains(response, "Tesla Model S")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "CBR-1000")

    def test_get_context_data_manufacturer_list_view(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "test111"}
        )
        self.assertIn("search_form", response.context)

    def test_search_car_with_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "NonExistingModel"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Tesla Model S")
        self.assertNotContains(response, "CBR-1000")

    def test_search_car_with_empty_query_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla Model S")
        self.assertContains(response, "CBR-1000")
