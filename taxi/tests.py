from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.
from taxi.models import Manufacturer, Car
from taxi.views import ManufacturerListView, CarListView, DriverListView


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="QWE43523"
        )
        self.client.login(username="testuser", password="testpass123")

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer2
        )

        self.driver2 = get_user_model().objects.create_user(
            username="againuser",
            password="testpass123",
            license_number="QWE56433"
        )

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toy"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_car_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Cor"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_driver_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertNotContains(response, "againuser")

    def test_search_forms_in_context(self):
        views = [
            ("taxi:manufacturer-list", ManufacturerListView),
            ("taxi:car-list", CarListView),
            ("taxi:driver-list", DriverListView),
        ]

        for url_name, view_class in views:
            url = reverse(url_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn("search_form", response.context)
