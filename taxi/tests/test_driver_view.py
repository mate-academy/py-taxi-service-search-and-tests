from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            license_number="TES12345",
        )
        self.client.force_login(self.user)

        self.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="123test",
            license_number="SET09876",
        )
        self.user3 = get_user_model().objects.create_user(
            username="testuser3",
            password="456test",
            license_number="KOL91123"
        )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_car_get_context_data(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "test"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], DriverSearchForm
        )
        self.assertEqual(
            response.context_data["search_form"].initial["username"], "test"
        )

    def test_get_query_with_no_filters(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.user3.username)

    def test_get_query_with_filters(self):
        response = self.client.get(
            DRIVER_LIST_URL, {"username": self.user2.username}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)
        self.assertNotContains(response, self.user3.username)
