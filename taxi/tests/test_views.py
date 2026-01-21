from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class SearchViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="test12345"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        self.manufacturer = Manufacturer.objects.first()
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": ""}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Cam"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)
