from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class TestPrivateViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_privet(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
