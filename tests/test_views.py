from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class DriverModelViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345",
        )
        self.client.login(username="testuser", password="12345")

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
