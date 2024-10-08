from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car, Manufacturer


class PublicAccessTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required_redirect(self):
        """Test that login is required for accessing protected pages."""
        protected_urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

    def test_logged_in_user_access(self):
        """Test that logged-in user can access all pages."""
        accessible_urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]

        for url in accessible_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
