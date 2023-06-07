from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PrivateDriverListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Bob",
            password="Test12345",
            license_number="TES12345"
        )
        self.user = get_user_model().objects.create_user(
            username="Dylan",
            password="Test12343",
            license_number="SET12345"
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_search_drivers(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "Bob"})
        search_driver = Driver.objects.filter(username="Bob")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(search_driver)
        )


class PublicDriverListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
