from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123",
            license_number="ASD12349"
        )
        get_user_model().objects.create_user(
            username="bob",
            password="test123",
            license_number="ASD12345"
        )
        get_user_model().objects.create_user(
            username="david",
            password="test123",
            license_number="ASD12346"
        )
        get_user_model().objects.create_user(
            username="james",
            password="test123",
            license_number="ASD12347"
        )
        self.client.login(username="admin", password="admin123")

    def test_search_by_username(self):
        response = self.client.get(
            DRIVER_URL,
            {"username": "james"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "james")
        self.assertNotContains(response, "david")
        self.assertNotContains(response, "bob")
        self.assertNotContains(response, "<td>admin</td>")

    def test_search_case_insensitive(self):
        response = self.client.get(
            DRIVER_URL,
            {"username": "AdMi"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin")
        self.assertNotContains(response, "bob")
        self.assertNotContains(response, "david")
        self.assertNotContains(response, "james")

    def test_empty_search_returns_all(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": ""}
        )

        self.assertContains(response, "admin")
        self.assertContains(response, "bob")
        self.assertContains(response, "james")
        self.assertContains(response, "david")
