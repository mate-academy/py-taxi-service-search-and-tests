from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVERS_URL = reverse("taxi:driver-list")


class PublicDriversTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertEqual(res.status_code, 302)


class TestDriverDetailView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password123",
            license_number="ASD45678",
        )
        self.client.force_login(self.user)

    def test_user_license_number_displayed(self):
        res = self.client.get(
            reverse("taxi:driver-detail", args=[self.user.pk])
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "ASD45678")
