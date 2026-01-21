from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchTests(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer", country="USA"
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="Another Manufacturer", country="USA"
        )

        self.car1 = Car.objects.create(
            model="Test Car", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Another Car", manufacturer=self.manufacturer2
        )

        self.user1 = get_user_model().objects.create_user(
            username="Test User",
            email="test2@mail.com",
            password="test1234!",
            license_number="CLA12345",
        )
        self.user2 = get_user_model().objects.create_user(
            username="Another",
            email="test2@mail.com",
            password="test12345!",
            license_number="CLA12346",
        )

        self.client.force_login(self.user1)
        self.client.force_login(self.user2)

    def test_manufacturer_name_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Test Manufacturer"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")
        self.assertNotContains(response, "Another Manufacturer")

    def test_manufacturer_name_search_with_no_data(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")
        self.assertContains(response, "Another Manufacturer")

    def test_car_model_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Test Car"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")
        self.assertNotContains(response, "Another Car")

    def test_car_model_search_with_no_data(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")
        self.assertContains(response, "Another Car")

    def test_driver_username_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "Test User"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")
        self.assertNotContains(response, "Another User")

    def test_driver_username_search_with_no_search_data(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": ""})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test User")
        self.assertContains(response, "Another")
